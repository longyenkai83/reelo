"""Journey → existing purified Planner → existing Writer/Critic/one prose repair.

NativeHost.invoke_stage is the production provider. Tests inject deterministic terminal
providers through the same envelope/schema/state machine; they are not live quality proof.
"""
import json
from pathlib import Path
from uuid import uuid4

from integrations.content_intelligence.adapter import ExecutionResult, encoded
from integrations.content_intelligence.contract import StrictModel, value_hash
from integrations.content_intelligence.context_packs import manifest, ROOT
from integrations.content_intelligence.purified_plan import validate, execution_view
from integrations.content_intelligence.stages import execute_stages, stage_identity, validate_envelope, persist
from .creative import JourneyCreativePlan
from .strategy import slot_context, verify_sources


class JourneyReceipt(StrictModel):
    campaign_id: str
    campaign_plan_hash: str
    slot_id: str
    context_hash: str


class JourneyExecution(ExecutionResult):
    receipt: JourneyReceipt


def _execution(digest, context):
    return JourneyExecution(receipt=JourneyReceipt(campaign_id=context['campaign']['campaign_id'],
        campaign_plan_hash=digest, slot_id=context['slot']['slot_id'], context_hash=value_hash(context)),
        generation_id='JGEN-'+uuid4().hex, parent_generation_id=None, status='RUNNING')


class JourneyEngine:
    def __init__(self, store, state_directory, invoke, read_files, *, current_insight=None):
        self.store, self.root, self.invoke = store, Path(state_directory), invoke
        self.read_files, self.current_insight = tuple(Path(p) for p in read_files), current_insight
        self.root.mkdir(parents=True, exist_ok=True)

    def context(self, digest, slot_id):
        plan = self.store.load(digest)
        return slot_context(plan, slot_id, memory=self.store.memory(digest), current_insight=self.current_insight)

    def assets(self, context):
        paths = list(self.read_files) + [Path(s['path']) for s in context['sources']]
        creator = context['campaign']['creator_id']
        # Recognized brand subfolders may never cross creator scope. Nonstandard
        # shared assets are explicit operator configuration, not fallback discovery.
        for path in paths:
            parts = path.as_posix().split('/')
            if 'brand' in parts and parts[parts.index('brand') + 1] != creator:
                raise ValueError('creator_asset_scope_mismatch')
        return manifest(paths, ROOT)

    def prepare(self, digest, slot_id):
        context = self.context(digest, slot_id)
        if any(e['plan_hash'] == digest and e['kind'] == 'EXECUTION_STARTED' and
               e['data']['slot_id'] == slot_id for e in self.store.events(context['campaign']['campaign_id'])):
            raise ValueError('slot_already_reserved_no_automatic_retry')
        assets = self.assets(context)
        execution = _execution(digest, context)
        work = self.root / execution.generation_id
        work.mkdir()
        inputs = dict(plan_route='reelo.journey-creative-plan.1', selected_mode=context['slot']['mode'],
                      plan_schema=JourneyCreativePlan.model_json_schema(), context_hash=value_hash(context))
        stage = stage_identity(execution, 'CREATIVE_PLAN', inputs)
        self.store.append(digest, 'PLANNER_STARTED', dict(slot_id=slot_id, generation_id=execution.generation_id))
        persist(work/'request.json', dict(context=context, assets=assets, stage=stage, inputs=inputs))
        try:
            body, host = self.invoke(execution, context, stage, inputs, work, assets)
            persist(work/'returned.json', dict(body=body, host=host))
            raw = validate_envelope(body, stage, context)
            proposal = validate(raw, context, assets)
            if not host.get('task_id') or not host.get('tool_use_id'): raise ValueError('stage_host_correlation_missing')
            if self.context(digest, slot_id) != context or self.assets(context) != assets:
                raise ValueError('planning_source_or_campaign_changed')
            record = dict(creative_plan_id='JCP-'+uuid4().hex, plan_revision=1,
                          plan_hash=value_hash(proposal), context_hash=value_hash(context),
                          proposal=proposal, context=context, assets=assets, host=host,
                          generation_id=execution.generation_id, slot_id=slot_id)
            persist(work/'plan.json', record)
            self.store.append(digest, 'CREATIVE_PLAN', record)
            return record
        except Exception as exc:
            self.store.append(digest, 'PLANNER_UNKNOWN', dict(slot_id=slot_id,
                generation_id=execution.generation_id, error=type(exc).__name__))
            raise

    def approve_sample_plan(self, digest, plan_id, *, reviewer, human_attested, authority_ref):
        if human_attested is not True or not reviewer.strip() or not authority_ref.strip():
            raise ValueError('explicit_human_instruction_required')
        plan = self._plan(digest, plan_id)
        self._current(digest, plan)
        return self.store.append(digest, 'CREATIVE_APPROVAL', dict(plan_id=plan_id, plan_hash=plan['plan_hash'],
            reviewer=reviewer, human_attested=True, actor_kind='human', authority_ref=authority_ref))

    def propose_terminal_revision(self, digest, generation_id, revised, *, operator, rationale):
        """A NEW pending proposal, not a rewrite of UNKNOWN or a continuation approval.

        Trusted operator may correct an unapproved terminal proposal. Require exact durable
        request/envelope/host evidence and current source scope. Models cannot call this.
        Individual real sample-plan approval is still required before a Guided Writer.
        """
        if not operator.strip() or not rationale.strip(): raise ValueError('revision_audit_required')
        work = (self.root / generation_id).resolve()
        if work.parent != self.root.resolve(): raise ValueError('invalid_generation_path')
        request = json.loads((work/'request.json').read_text(encoding='utf8'))
        returned = json.loads((work/'returned.json').read_text(encoding='utf8'))
        context = request['context']; stage = request['stage']
        if (stage['generation_id'] != generation_id or stage['campaign_plan_hash'] != digest or
                stage['input_hash'] != value_hash(request['inputs'])):
            raise ValueError('revision_parent_identity_invalid')
        validate_envelope(returned['body'], stage, context)
        if not returned['host'].get('task_id') or not returned['host'].get('tool_use_id'):
            raise ValueError('stage_host_correlation_missing')
        if self.context(digest, context['slot']['slot_id']) != context or self.assets(context) != request['assets']:
            raise ValueError('revision_sources_not_current')
        events=self.store.events(context['campaign']['campaign_id'])
        if not any(e['plan_hash']==digest and e['kind']=='PLANNER_UNKNOWN' and
                   e['data']['generation_id']==generation_id for e in events):
            raise ValueError('revision_requires_recorded_rejected_parent')
        proposal = validate(revised, context, request['assets'])
        record = dict(creative_plan_id='JCP-'+uuid4().hex,plan_revision=1,plan_hash=value_hash(proposal),
            context_hash=value_hash(context),proposal=proposal,context=context,assets=request['assets'],
            host=returned['host'],generation_id='JDER-'+uuid4().hex,slot_id=context['slot']['slot_id'],
            origin='OPERATOR_DERIVED_PENDING_REVIEW',parent_native_generation_id=generation_id,
            revision_audit=dict(operator=operator,rationale=rationale,parent_output_hash=value_hash(returned['body']['output']),
                                human_approval_inherited=False,original_unknown_preserved=True))
        self.store.append(digest,'CREATIVE_PLAN',record)
        persist(work / (record['creative_plan_id']+'-derived.json'),record)
        return record

    def _plan(self, digest, plan_id):
        campaign = self.store.load(digest)
        plans = [e['data'] for e in self.store.events(campaign.request.campaign_id)
                 if e['plan_hash'] == digest and e['kind'] == 'CREATIVE_PLAN']
        chosen = next(p for p in plans if p['creative_plan_id'] == plan_id)
        if [p for p in plans if p['slot_id'] == chosen['slot_id']][-1] != chosen:
            raise ValueError('creative_plan_superseded')
        return chosen

    def _current(self, digest, plan):
        if (self.context(digest, plan['slot_id']) != plan['context'] or
                self.assets(plan['context']) != plan['assets'] or
                value_hash(plan['proposal']) != plan['plan_hash']):
            raise ValueError('creative_plan_or_context_not_current')
        validate(plan['proposal'], plan['context'], plan['assets'])

    def _authorization(self, digest, plan):
        scope = self.store.load(digest)
        authority = self.store.authority(digest, sample=True)
        if authority:
            return dict(kind='campaign_execution', event_id=authority['event_id'],
                        individual_human_creative_approval=False)
        approvals = [e for e in self.store.events(scope.request.campaign_id)
                     if e['plan_hash'] == digest and e['kind'] == 'CREATIVE_APPROVAL'
                     and e['data']['plan_id'] == plan['creative_plan_id'] and e['data']['plan_hash'] == plan['plan_hash']]
        if not approvals: raise ValueError('real_sample_creative_approval_required')
        return dict(kind='human_creative_approval', event_id=approvals[-1]['event_id'],
                    individual_human_creative_approval=True)

    def run(self, digest, plan_id):
        plan = self._plan(digest, plan_id)
        self._current(digest, plan)
        authority = self._authorization(digest, plan)
        context, assets, p = plan['context'], plan['assets'], plan['proposal']
        events = self.store.events(context['campaign']['campaign_id'])
        for dep in context['slot']['dependencies']:
            if not any(e['plan_hash'] == digest and e['kind'] == 'RESULT' and
                       e['data']['slot_id'] == dep and e['data']['status'] == 'DRAFT_READY' for e in events):
                raise ValueError('prior_slot_not_completed')
        if any(e['plan_hash'] == digest and e['kind'] == 'EXECUTION_STARTED' and
               e['data']['slot_id'] == plan['slot_id'] for e in events):
            raise ValueError('slot_already_reserved_no_automatic_retry')
        view = execution_view(p)
        approved = dict(decision='authorized_campaign_execution', authority_kind=authority,
            plan={k: plan[k] for k in ('creative_plan_id', 'plan_revision', 'plan_hash', 'context_hash', 'proposal')},
            selected_hook=p['opening_plan']['recommended'], selected_title=p['title_plan']['recommended'],
            selected_mode=p['format'], selected_story_refs=view['story_matches'],
            selected_knowledge_refs=view['knowledge_matches'], psychology=p['psychology'],
            knowledge_choice_policy='Only the selected source contributions; no forced extra source.')
        original = encoded(approved)
        def recheck():
            self._current(digest, plan)
            if self._plan(digest, plan_id) != plan or self._authorization(digest, plan) != authority:
                raise ValueError('campaign_authority_changed')
            return json.loads(original)
        execution = _execution(digest, context)
        work = self.root / execution.generation_id
        work.mkdir()
        self.store.append(digest, 'EXECUTION_STARTED', dict(slot_id=plan['slot_id'], generation_id=execution.generation_id))
        result = execute_stages(execution, context, work, assets, self.invoke,
                                approved_plan=approved, recheck_approval=recheck)
        final = result.artifacts[-1] if result.artifacts else None
        slot = context['slot']
        self.store.append(digest, 'RESULT', dict(slot_id=slot['slot_id'], status=result.status,
            generation_id=result.generation_id, draft_hash=final['content_hash'] if final else None,
            stage=slot['journey_stage'], source_ids=context['source_ids'], topic=slot['topic'],
            one_idea=slot['one_idea'], content_job=slot['content_job'], cta_intent=slot['cta_intent'],
            hook=p['opening_plan']['recommended']['text'], title=p['title_plan']['recommended']['text'],
            next_intended_stage=slot['next_intended_stage'], human_final_approval='PENDING', published=False))
        return result

    def execute_remaining(self, digest):
        plan = self.store.load(digest)
        self.store.authority(digest)  # no preparation or launch without bounded authority
        results = []
        for slot in plan.sequence:
            completed = self.store.memory(digest)['completed']
            if any(r['slot_id'] == slot.slot_id and r['status'] == 'DRAFT_READY' for r in completed): continue
            proposal = self.prepare(digest, slot.slot_id)
            result = self.run(digest, proposal['creative_plan_id'])
            results.append(result)
            if result.status != 'DRAFT_READY': break
        return results
