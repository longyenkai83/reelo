"""E1 plan authority; legacy-shaped views below are derived, never stored as a second plan."""
from copy import deepcopy
from pathlib import Path
from typing import Literal
import hashlib

from pydantic import Field
from .creative_plan import Model, Candidate, Psychology, SourceMatch
from .context_packs import validate_recipe, asset_id, selected_section

ROUTE = 'reelo.creative-plan.e1'
JOURNEY_ROUTE = 'reelo.journey-creative-plan.1'


class Movement(Model):
    start_state: str = Field(min_length=1)
    tension_or_question: str = Field(min_length=1)
    change_or_turn: str | None = None
    end_state: str = Field(min_length=1)


class ReelOpening(Model):
    spoken: str
    text: str
    visual: str
    audio: str | None = None


class Opening(Model):
    recommended: Candidate
    alternative: Candidate | None = None
    reel_package: ReelOpening | None = None


class Title(Model):
    recommended: Candidate
    alternative: Candidate | None = None


class Proof(Model):
    kind: Literal['CUSTOMER_EVIDENCE', 'CREATOR_STORY', 'CREATOR_KNOWLEDGE',
                  'EXTERNAL_KNOWLEDGE', 'ILLUSTRATIVE_AI', 'NONE']
    supports: str = Field(min_length=1)
    requires_factual_support: bool
    evidence_ids: list[str] = Field(default_factory=list)
    source: SourceMatch | None = None
    contribution: str = Field(min_length=1)
    disclosure: str | None = None


class Safety(Model):
    truth_preserved: bool
    selected_intent_preserved: bool
    reader_centered_pov: bool
    non_prescriptive_tone: bool
    reader_value_clear: bool
    narrative_payoff_clear: bool


class CompatibilityTitle(Model):
    candidate: Candidate
    frame: str = Field(min_length=1)  # SELF_MADE or an exact section of selected title source.
    frame_reference_id: str | None = None


class PurifiedPlan(Model):
    schema_version: Literal['reelo.creative-plan.e1']
    # Platform identity is distinct from the semantic plan fields below.
    packet_id: str
    verified_insight_id: str
    angle_id: str
    truth_type: Literal['PROPOSED']
    format: Literal['REEL', 'SHORT_ARTICLE', 'LONG_ARTICLE']
    one_idea: str = Field(min_length=1)
    reader_value: list[str] = Field(min_length=1)
    content_job: str
    recipe_id: str
    proof_plan: list[Proof] = Field(min_length=1)
    emotional_movement: Movement
    opening_plan: Opening
    title_plan: Title
    outline: list[str] = Field(min_length=1)
    payoff: str = Field(min_length=1)
    cta_direction: str
    psychology: Psychology | Literal['NONE']
    limitations: list[str] = Field(default_factory=list)
    advisories: list[str] = Field(default_factory=list)
    publication_requirements: list[str] = Field(default_factory=list)
    safety: Safety
    blocking_issues: list[str] = Field(default_factory=list)
    # Internal title-eight appendix. Primary selected texts live only in title_plan.
    compatibility_titles: list[CompatibilityTitle] = Field(min_length=1, max_length=4)
    selected_title_frame: str = 'SELF_MADE'
    selected_title_frame_reference_id: str | None = None


def is_purified(p):
    return p.get('schema_version') in (ROUTE, JOURNEY_ROUTE)


def components(component):
    return [component['recommended']] + ([component['alternative']] if component.get('alternative') else [])


def execution_view(p):
    if not is_purified(p): return p
    view = {k: p[k] for k in ('packet_id', 'verified_insight_id', 'angle_id', 'truth_type', 'format',
        'content_job', 'recipe_id', 'reader_value', 'outline', 'psychology', 'cta_direction',
        'limitations', 'advisories', 'publication_requirements', 'blocking_issues')}
    view.update(p['safety'])
    view.update(story_matches=[], knowledge_matches=[], illustrations=[], narrative_payoffs=[],
                treatment_or_truc=p['emotional_movement']['tension_or_question'], creative_constraints=[],
                hook_candidates=components(p['opening_plan']),
                title_candidates=components(p['title_plan']) + [r['candidate'] for r in p['compatibility_titles']],
                recommended_hook_id=p['opening_plan']['recommended']['candidate_id'],
                recommended_title_id=p['title_plan']['recommended']['candidate_id'])
    for proof in p['proof_plan']:
        source = proof['source']
        if proof['kind'] in ('CREATOR_STORY', 'CLIENT_STORY'):
            view['story_matches'].append(source)
            movement = p['emotional_movement']
            view['narrative_payoffs'].append(dict(source_ref=source['source_ref'], section=source['section'],
                story_job=proof['contribution'], setup=movement['start_state'],
                tension_or_turn=movement['tension_or_question'], meaning=proof['contribution'], reader_payoff=p['payoff']))
        elif source is not None:
            view['knowledge_matches'].append(source)
        elif proof['kind'] == 'ILLUSTRATIVE_AI':
            view['illustrations'].append(dict(description=proof['supports'], origin='illustrative_ai', disclosure=proof['disclosure']))
    return view


def validate(raw, context, assets):
    from .creative_plan import source_role
    from .evidence_context import is_journey, evidence
    journey = is_journey(context)
    if journey:
        from integrations.journey.creative import JourneyCreativePlan, validate_identity, validate_proof_source
        p = JourneyCreativePlan.model_validate(raw).model_dump()
        validate_identity(p, context)
    else:
        p = PurifiedPlan.model_validate(raw).model_dump()
    if any(not p[k].strip() for k in ('one_idea', 'payoff')) or any(
            not p['emotional_movement'][k].strip() for k in ('start_state', 'tension_or_question', 'end_state')):
        raise ValueError('incomplete_purified_plan')
    validate_recipe(p['content_job'], p['recipe_id'])
    if not journey:
        packet = context['packet']; insight = packet['customer_truth']['verified_insight']
        if (p['packet_id'], p['verified_insight_id'], p['angle_id']) != (
                packet['packet_id'], insight['verified_insight_id'], packet['content_strategy']['angle']['angle_id']):
            raise ValueError('plan_upstream_identity_mismatch')
    refs = {r['evidence_id'] for r in evidence(context)[0]}
    allowed = {a['path']: a for a in assets}
    by_id = {asset_id(a['path']): a for a in assets}
    for proof in p['proof_plan']:
        kind = proof['kind']; source = proof['source']
        if not set(proof['evidence_ids']) <= refs: raise ValueError('invalid_proof_evidence_identity')
        if kind in ('NONE', 'ILLUSTRATIVE_AI'):
            if proof['requires_factual_support'] or source or proof['evidence_ids']:
                raise ValueError('nonfactual_proof_cannot_support_factual_claim')
            if kind == 'ILLUSTRATIVE_AI' and not (proof['disclosure'] or '').strip():
                raise ValueError('illustration_disclosure_required')
        elif kind == 'CUSTOMER_EVIDENCE':
            if not proof['evidence_ids'] or source: raise ValueError('customer_evidence_required')
        elif journey:
            validate_proof_source(proof, context, allowed)
        else:
            if not source or proof['evidence_ids']: raise ValueError('proof_source_required')
            path = Path(source['source_ref']).as_posix()
            if path not in allowed or allowed[path]['sha256'] != source['sha256']:
                raise ValueError('plan_source_origin_invalid')
            raw_source = Path(path).read_bytes()
            if hashlib.sha256(raw_source).hexdigest() != source['sha256']: raise ValueError('approved_source_changed')
            creator = kind.startswith('CREATOR_')
            expected_origin = {'CREATOR_STORY': 'creator_story', 'CREATOR_KNOWLEDGE': 'creator_observation',
                               'EXTERNAL_KNOWLEDGE': 'external_knowledge'}[kind]
            if source_role(path) != ('creator' if creator else 'knowledge') or source['origin'] != expected_origin:
                raise ValueError('plan_source_origin_invalid')
            section = selected_section(raw_source.decode('utf-8-sig'), source['section'])
            if not source['support_quote'].strip() or source['support_quote'] not in section:
                raise ValueError('proof_support_not_in_source')
            if not source['allowed_use'].strip() or not source['why_relevant'].strip():
                raise ValueError('plan_source_use_missing')
    if p['psychology'] != 'NONE':
        psy = p['psychology']; ref = psy['reference_id']
        if ref not in by_id: raise ValueError('psychology_reference_identity_required')
        a = by_id[ref]
        if 'nguyen-ly-tam-ly' not in a['path']: raise ValueError('invalid_psychology_reference')
        if psy['library_source'] and Path(psy['library_source']).as_posix() != a['path']:
            raise ValueError('psychology_reference_identity_mismatch')
        raw_library = Path(a['path']).read_bytes()
        if hashlib.sha256(raw_library).hexdigest() != a['sha256']: raise ValueError('approved_source_changed')
        text = ' '.join(raw_library.decode('utf-8-sig').casefold().split())
        for name in (psy['primary_mechanism'], psy['optional_secondary_mechanism']):
            if name is not None and (not name.strip() or ' '.join(name.casefold().split()) not in text):
                raise ValueError('psychology_mechanism_not_in_library')
        psy['library_source'] = a['path']
    view = execution_view(p)
    if len(p['reader_value']) != len(p['outline']) or any(not x.strip() for x in p['outline'] + p['reader_value']):
        raise ValueError('reader_value_required_for_every_section')
    for name in ('hook_candidates', 'title_candidates'):
        candidates = view[name]; ids = [c['candidate_id'] for c in candidates]
        if len(set(ids)) != len(ids): raise ValueError('invalid_candidate_selection')
        texts = [' '.join(c['text'].casefold().split()) for c in candidates]
        if len(set(texts)) != len(texts): raise ValueError('duplicate_component_wording')
        for c in candidates:
            candidate_refs = refs | set(context['source_ids']) if journey else refs
            if not c['text'].strip() or not c['rationale'].strip() or not set(c['evidence_refs']) <= candidate_refs:
                raise ValueError('invalid_candidate_provenance')
    if not 3 <= len(view['title_candidates']) <= 5: raise ValueError('title_eight_compatibility_table_required')
    rows = [(p['selected_title_frame'], p['selected_title_frame_reference_id'])]
    rows += [(r['frame'], r['frame_reference_id']) for r in p['compatibility_titles']]
    # A title alternative is self-made unless it is made primary in a new revision.
    for frame, ref in rows:
        if frame == 'SELF_MADE':
            if ref is not None: raise ValueError('self_made_frame_has_no_library_identity')
        else:
            if ref not in by_id or Path(by_id[ref]['path']).name != 'bo-tieu-de.md':
                raise ValueError('title_frame_reference_required')
            a = by_id[ref]; raw_frame = Path(a['path']).read_bytes()
            if hashlib.sha256(raw_frame).hexdigest() != a['sha256']: raise ValueError('approved_source_changed')
            selected_section(raw_frame.decode('utf-8-sig'), frame)
    if p['format'] != 'REEL' and p['opening_plan']['reel_package'] is not None:
        raise ValueError('written_mode_cannot_require_reel_package')
    return p


def gate(p):
    result = {k: deepcopy(p[k]) for k in ('one_idea', 'reader_value', 'content_job', 'recipe_id',
        'proof_plan', 'emotional_movement', 'opening_plan', 'title_plan', 'outline', 'payoff',
        'cta_direction', 'limitations', 'advisories', 'publication_requirements', 'format', 'psychology')}
    for key in ('opening_plan', 'title_plan'):
        for choice in ('recommended', 'alternative'):
            candidate = result[key].get(choice)
            if candidate:
                result[key][choice] = {k: candidate[k] for k in ('candidate_id', 'text', 'rationale')}
    return result


def title_table(p):
    primary = [dict(candidate=c, frame=p['selected_title_frame'] if i == 0 else 'SELF_MADE',
                    frame_reference_id=p['selected_title_frame_reference_id'] if i == 0 else None)
               for i, c in enumerate(components(p['title_plan']))]
    return [dict(r, psychology=p['psychology'], treatment=p['emotional_movement']['tension_or_question'])
            for r in primary + p['compatibility_titles']]
