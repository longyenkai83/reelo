"""Explore slots sequentially using one proposal provider and actual campaign memory."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from integrations.content_intelligence.context_packs import selected_section
from integrations.content_intelligence.contract import ContentIntelligencePacket
from .models import JourneyPlan, Slot
from .models import STAGES, COMMERCIAL


def read_source(source):
    path = Path(source.path)
    if not path.is_absolute(): raise ValueError('absolute_source_path_required')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != source.sha256: raise ValueError('source_hash_changed:' + source.source_id)
    if source.kind == 'VERIFIED_INSIGHT':
        packet = ContentIntelligencePacket.model_validate_json(raw)
        if packet.packet_id != source.packet_id: raise ValueError('source_packet_identity_mismatch')
        return packet.model_dump(mode='json')
    if source.kind == 'CLIENT_STORY':
        if not source.permission_ref or not source.permission_sha256:
            raise ValueError('client_story_permission_required')
        permission = Path(source.permission_ref)
        if not permission.is_absolute() or hashlib.sha256(permission.read_bytes()).hexdigest() != source.permission_sha256:
            raise ValueError('client_story_permission_changed')
        grant = json.loads(permission.read_text(encoding='utf-8-sig'))
        if (grant.get('source_id') != source.source_id or grant.get('source_sha256') != source.sha256 or
                grant.get('creator_id') != source.creator_id or grant.get('human_attested') is not True or
                not grant.get('reviewer') or grant.get('scope') != 'content_drafting' or grant.get('revoked') is not False):
            raise ValueError('client_story_permission_scope_invalid')
    return selected_section(raw.decode('utf-8-sig'), source.section)


def verify_sources(plan, current_insight=None, *, source_ids=None):
    """Caller supplies producer-owned CURRENT ledger check; snapshots alone never authorize CI."""
    bodies = {}
    for source in plan.sources:
        if source_ids is not None and source.source_id not in source_ids: continue
        body = read_source(source)
        if source.kind == 'VERIFIED_INSIGHT':
            if current_insight is None: raise ValueError('current_insight_authority_required')
            # Must raise for stale/revoked. No boolean from model or catalog is accepted.
            current_insight(body)
        bodies[source.source_id] = body
    return bodies


def explore(request, sources, propose_slot, *, history=()):
    """No fixed ten-step ladder or allocation. Provider chooses MOVE/REINFORCE from scope.

    The provider sees prior proposed slots AND actual history; neither is source truth.
    A source catalog alone is metadata; selected source bytes need independent validation.
    """
    sequence = []
    for index in range(request.content_count):
        context = dict(request=request.model_dump(), source_catalog=[s.model_dump() for s in sources],
                       prior_slots=deepcopy(sequence), editorial_history=deepcopy(list(history)),
                       slot_number=index + 1, strategy_truth_type='PROPOSED',
                       instruction='Select exactly one primary; add at most two supports only with useful contributions. '
                       'Do not infer beliefs or demand from stage. History is not customer evidence. '
                       'CTA intent follows the journey, wording follows creator voice. No publication.')
        slot = Slot.model_validate(propose_slot(context))
        sequence.append(slot.model_dump())
    return JourneyPlan.model_validate(dict(request=request.model_dump(), sources=[s.model_dump() for s in sources],
                                          sequence=sequence, editorial_history=deepcopy(list(history))))


def propose_flow(request, sources, *, history=(), stage_sequence=None):
    """Small deterministic starting proposal, replaceable by the same explore provider.

    Exact topic catalog matching, least-used source first. Not semantic retrieval and not
    proof of campaign effectiveness. Optional explicit stage sequence handles reinforcement,
    mixed goals and timing; default distributes only across the requested start/target range.
    Never inserts supporting fuel simply to satisfy a template.
    """
    start, end = (STAGES.index(request.starting_awareness_stage), STAGES.index(request.target_awareness_stage))
    if stage_sequence is None:
        stage_sequence = [STAGES[start + (end - start) * i // max(1, request.content_count - 1)]
                          for i in range(request.content_count)]
    if len(stage_sequence) != request.content_count or stage_sequence[0] != request.starting_awareness_stage:
        raise ValueError('stage_sequence_scope_mismatch')
    meanings = {'UNAWARE': 'recognize a relevant situation', 'PROBLEM_AWARE': 'name a question or struggle without diagnosis',
        'SOLUTION_AWARE': 'understand an approach and its limits', 'PRODUCT_AWARE': 'evaluate the actual approach or offer',
        'MOST_AWARE': 'choose an appropriate next step with clear conditions'}
    eligible = {'STORY_LED': {'CREATOR_STORY', 'CREATOR_EXPERIENCE', 'CLIENT_STORY'},
        'INSIGHT_LED': {'VERIFIED_INSIGHT'},
        'KNOWLEDGE_POV_LED': {'CREATOR_KNOWLEDGE_POV', 'EXTERNAL_KNOWLEDGE', 'MARKET_OBSERVATION', 'FUTURE_POSSIBILITY'}}
    def propose(context):
        i = context['slot_number'] - 1
        stage = stage_sequence[i]
        nxt = stage_sequence[i + 1] if i + 1 < len(stage_sequence) else request.target_awareness_stage
        used = [s['primary_source']['source_id'] for s in context['prior_slots']]
        used += [sid for row in history for sid in row.get('source_ids', [])]
        candidates = [s for s in sources if set(s.topics) & set(request.topics)
                      and (request.route == 'AUTO_DISCOVERY' or s.kind in eligible[request.route])
                      and not (stage in ('UNAWARE','PROBLEM_AWARE') and s.kind == 'OFFER_BUSINESS_CONTEXT')]
        if not candidates: raise ValueError('no_matching_primary_source')
        chosen = min(candidates, key=lambda s: (used.count(s.source_id), s.source_id))
        topic = next(t for t in request.topics if t in chosen.topics)
        candidates_cta = [c for c in request.allowed_cta_intents if
            c not in COMMERCIAL or (request.offer_context and (c == 'EXPLORE_OFFER' and stage in ('PRODUCT_AWARE', 'MOST_AWARE')
                                                              or c == 'BOOK_BUY_APPLY' and stage == 'MOST_AWARE'))]
        if not candidates_cta: raise ValueError('no_safe_cta_in_scope')
        priority = {'UNAWARE': ['REFLECT','ENGAGE','SAVE_FOLLOW'], 'PROBLEM_AWARE': ['ENGAGE','SAVE_FOLLOW','REFLECT'],
                    'SOLUTION_AWARE': ['LEARN_METHOD','GET_RESOURCE','ASK_DM'],
                    'PRODUCT_AWARE': ['EXPLORE_OFFER','ASK_DM','LEARN_METHOD'],
                    'MOST_AWARE': ['BOOK_BUY_APPLY','EXPLORE_OFFER','ASK_DM']}[stage]
        cta = next((c for c in priority if c in candidates_cta), candidates_cta[0])
        job = 'STORY' if chosen.kind in ('CREATOR_STORY','CLIENT_STORY','CREATOR_EXPERIENCE') else (
            'REFLECT' if chosen.kind in ('VERIFIED_INSIGHT','CUSTOMER_VOICE','FUTURE_POSSIBILITY') else 'TEACH')
        prior_jobs = ', '.join(s['slot_id'] + ':' + s['content_job'] for s in context['prior_slots']) or 'none assigned yet'
        idea = (read_source(chosen)['content_strategy']['angle']['core_argument']['text'] if chosen.kind == 'VERIFIED_INSIGHT'
                else f'{chosen.summary} — proposed lens: {meanings[stage]}')
        supporting = []
        required_source = request.offer_context.source_id if cta in COMMERCIAL else (
            request.resource_source_id if cta == 'GET_RESOURCE' else None)
        if required_source and required_source != chosen.source_id:
            supporting.append(dict(source_id=required_source, contribution='Ground the actual offer/resource in the selected CTA'))
        return dict(slot_id=f'slot-{i+1}', order=i+1, journey_stage=stage, next_intended_stage=nxt,
            journey_objective=f'{meanings[stage]} through {topic}. Prior assigned work: {prior_jobs}',
            movement='REINFORCE' if stage == nxt else 'MOVE', one_idea=idea,
            topic=topic, content_job=job, recipe_id='c1:'+job,
            primary_source=dict(source_id=chosen.source_id, contribution=meanings[stage]), supporting_sources=supporting,
            reader_value=f'{meanings[stage]}; bounded by the selected source, not assumed audience beliefs',
            cta_intent=cta, mode=request.modes[i % len(request.modes)],
            dependencies=[s['slot_id'] for s in context['prior_slots']])
    return explore(request, sources, propose, history=history)


def slot_context(plan, slot_id, *, memory, current_insight=None):
    slot = next(s for s in plan.sequence if s.slot_id == slot_id)
    selected = [slot.primary_source, *slot.supporting_sources]
    ids = {u.source_id for u in selected}
    # Offer/resource fuel is counted in the same primary + max-two-support bound.
    bodies = verify_sources(plan, current_insight, source_ids=ids)
    sources = [s for s in plan.sources if s.source_id in ids]
    packets = [bodies[s.source_id] for s in sources if s.kind == 'VERIFIED_INSIGHT']
    if len(packets) > 1: raise ValueError('one_selected_insight_packet_per_piece')
    if packets and slot.one_idea != packets[0]['content_strategy']['angle']['core_argument']['text']:
        raise ValueError('journey_cannot_replace_selected_insight_angle')
    return dict(schema_version='reelo.journey-context.1', campaign=plan.request.model_dump(),
                slot=slot.model_dump(), prior_slots=[s.model_dump() for s in plan.sequence if s.order < slot.order],
                memory=dict(deepcopy(memory), imported_editorial_history=deepcopy(plan.editorial_history)), sources=[dict(s.model_dump(), text=bodies[s.source_id])
                                                for s in sources if s.kind != 'VERIFIED_INSIGHT'],
                packet=packets[0] if packets else None,
                strategy_truth_type='PROPOSED', audience_state_is_observed=False,
                source_ids=sorted(ids), publish_authorized=False)
