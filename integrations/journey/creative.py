"""Journey identity plus the SAME purified expression plan and validation mechanism."""
from pathlib import Path
from typing import Literal
import hashlib
from pydantic import Field
from integrations.content_intelligence.creative_plan import SourceMatch
from integrations.content_intelligence.purified_plan import PurifiedPlan, Proof
from integrations.content_intelligence.contract import value_hash
from integrations.content_intelligence.context_packs import selected_section


class JourneySourceMatch(SourceMatch):
    origin: Literal['creator_story', 'creator_observation', 'external_knowledge', 'client_story',
                    'market_observation', 'future_possibility', 'business_context', 'customer_speech']


class JourneyProof(Proof):
    kind: Literal['CUSTOMER_EVIDENCE', 'CREATOR_STORY', 'CREATOR_KNOWLEDGE', 'EXTERNAL_KNOWLEDGE',
                  'ILLUSTRATIVE_AI', 'NONE', 'CLIENT_STORY', 'MARKET_OBSERVATION',
                  'FUTURE_POSSIBILITY', 'BUSINESS_CONTEXT', 'CUSTOMER_SPEECH']
    source: JourneySourceMatch | None = None


class JourneyCreativePlan(PurifiedPlan):
    schema_version: Literal['reelo.journey-creative-plan.1']
    # Null means absent, never a synthetic Verified Insight for a creator-led piece.
    packet_id: str | None = None
    verified_insight_id: str | None = None
    angle_id: str | None = None
    campaign_id: str
    slot_id: str
    context_hash: str
    proof_plan: list[JourneyProof] = Field(min_length=1)


def validate_identity(p, context):
    slot = context['slot']
    if (p['campaign_id'] != context['campaign']['campaign_id'] or p['slot_id'] != slot['slot_id']
            or p['context_hash'] != value_hash(context)):
        raise ValueError('journey_plan_identity_mismatch')
    for key in ('one_idea', 'content_job', 'recipe_id'):
        if p[key] != slot[key]: raise ValueError('journey_slot_intent_changed')
    if p['format'] != slot['mode']: raise ValueError('journey_slot_mode_changed')
    if p['cta_direction'] != slot['cta_intent']: raise ValueError('journey_cta_intent_changed')
    packet = context.get('packet')
    identity = (packet['packet_id'], packet['customer_truth']['verified_insight']['verified_insight_id'],
                packet['content_strategy']['angle']['angle_id']) if packet else (None, None, None)
    if (p['packet_id'], p['verified_insight_id'], p['angle_id']) != identity:
        raise ValueError('journey_customer_identity_changed')
    # A primary source must actually contribute, not merely appear in metadata.
    uses = [slot['primary_source'], *slot['supporting_sources']]
    for use in uses:
        source = next((s for s in context['sources'] if s['source_id'] == use['source_id']), None)
        if source:
            if not any(proof['source'] and proof['source']['source_ref'] == source['path'] and
                       proof['source']['section'] == source['section'] for proof in p['proof_plan']):
                raise ValueError('selected_source_contribution_missing')
        elif not any(proof['kind'] == 'CUSTOMER_EVIDENCE' for proof in p['proof_plan']):
            raise ValueError('selected_insight_contribution_missing')
    if p['blocking_issues'] or not all(p['safety'].values()): raise ValueError('creative_plan_not_safe')
    for component in ('opening_plan', 'title_plan'):
        choice = p[component]['recommended']
        if choice['blocking_reasons'] or not all(choice[k] for k in
                ('intent_preserved', 'factual_claims_supported', 'natural_and_meaningful')):
            raise ValueError('recommended_component_not_safe')
    if packet:
        required = [r['strategy_field'] for r in packet['external_evidence_requirements']]
        if not set(required) <= set(p['publication_requirements']):
            raise ValueError('journey_packet_requirements_missing')


def validate_proof_source(proof, context, assets):
    source = proof['source']
    if not source or proof['evidence_ids']: raise ValueError('proof_source_required')
    allowed = [s for s in context['sources'] if s['path'] == source['source_ref'] and s['section'] == source['section']]
    if len(allowed) != 1: raise ValueError('source_outside_selected_fuel')
    selected = allowed[0]
    expected = {
        'CREATOR_STORY': ('CREATOR_STORY', 'creator_story'),
        'CREATOR_EXPERIENCE': ('CREATOR_STORY', 'creator_story'),
        'CLIENT_STORY': ('CLIENT_STORY', 'client_story'),
        'CREATOR_KNOWLEDGE_POV': ('CREATOR_KNOWLEDGE', 'creator_observation'),
        'EXTERNAL_KNOWLEDGE': ('EXTERNAL_KNOWLEDGE', 'external_knowledge'),
        'MARKET_OBSERVATION': ('MARKET_OBSERVATION', 'market_observation'),
        'FUTURE_POSSIBILITY': ('FUTURE_POSSIBILITY', 'future_possibility'),
        'OFFER_BUSINESS_CONTEXT': ('BUSINESS_CONTEXT', 'business_context'),
        'CUSTOMER_VOICE': ('CUSTOMER_SPEECH', 'customer_speech'),
    }[selected['kind']]
    if (proof['kind'], source['origin']) != expected: raise ValueError('source_role_laundering')
    path = Path(source['source_ref']).as_posix()
    if path not in assets or assets[path]['sha256'] != source['sha256'] or source['sha256'] != selected['sha256']:
        raise ValueError('plan_source_origin_invalid')
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != source['sha256']: raise ValueError('approved_source_changed')
    text = selected_section(raw.decode('utf-8-sig'), source['section'])
    if not source['support_quote'].strip() or source['support_quote'] not in text:
        raise ValueError('proof_support_not_in_source')
    if not source['allowed_use'].strip() or not source['why_relevant'].strip():
        raise ValueError('plan_source_use_missing')
    if source['use_as_same_situation'] and (source['match_type'] != 'DIRECT' or not source['same_situation_supported']):
        raise ValueError('adjacent_story_cannot_be_same_situation')
    if selected['kind'] == 'FUTURE_POSSIBILITY' and selected['truth_type'] not in ('HYPOTHESIS', 'PROPOSED'):
        raise ValueError('future_possibility_is_not_observed')
