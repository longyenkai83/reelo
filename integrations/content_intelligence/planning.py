"""One bounded Planner invocation. Its terminal result waits for a non-model review."""
import json
import time
from .adapter import encoded
from .contract import value_hash
from .creative_plan import PlanProposal, validate_proposal, source_role
from .stages import stage_identity, validate_envelope, persist


def execute_plan(execution, context, work, assets, invoke, store):
    inputs = dict(plan_schema=PlanProposal.model_json_schema(),
                  asset_roles=[dict(a, role=source_role(a['path'])) for a in assets])
    stage = stage_identity(execution, 'CREATIVE_PLAN', inputs)
    stage_dir = work/'CREATIVE_PLAN'; stage_dir.mkdir()
    persist(stage_dir/'request.json', dict(stage=stage, inputs=inputs, context=context, assets=assets))
    started = time.monotonic()
    record = dict(stage, status='CREATIVE_PLAN_RUNNING')
    execution.host = dict(profile='phase9-stage-wise', stages=[record], assets=assets)
    try:
        body, host = invoke(execution.model_copy(deep=True), json.loads(encoded(context)), stage, inputs, stage_dir, assets)
        raw = validate_envelope(body, stage, context)
        proposal = validate_proposal(raw, context, assets)
        if not host.get('task_id') or not host.get('tool_use_id'): raise ValueError('stage_host_correlation_missing')
        record.update(status='CREATIVE_PLAN_COMPLETED', raw=raw, normalized=proposal,
                      artifact_hash=value_hash(raw), normalized_hash=value_hash(proposal),
                      elapsed_seconds=round(time.monotonic()-started, 3), host=host)
        persist(stage_dir/'completed.json', record)
        plan = store.save(proposal, context, assets, execution.generation_id)
        execution.host['creative_plan'] = plan
        execution.validation_issues = plan['blockers']
        execution.status = 'PLAN_BLOCKED' if plan['blockers'] else 'PLAN_PENDING_APPROVAL'
        persist(work/'creative-plan.json', plan)
    except Exception as exc:
        import re
        code = str(exc) if re.fullmatch('[a-z][a-z0-9_]+', str(exc)) else 'planner_validation_or_host_failure'
        record.update(status='CREATIVE_PLAN_UNKNOWN', issue=code,
                      elapsed_seconds=round(time.monotonic()-started, 3))
        persist(stage_dir/'unknown.json', record)
        execution.status = 'UNKNOWN'; execution.validation_issues = [code]
    persist(work/'result.json', execution.model_dump(mode='json'))
    return execution
