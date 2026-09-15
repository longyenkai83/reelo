"""Bounded contract port from Insight ca09ae4d. No extraction or governance engine imports.
Source module hashes recorded in contract-provenance.json. Update only with parity tests.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

TruthType = Literal['OBSERVED', 'DERIVED']

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class SignalSource(StrictModel):
    comment_id: str
    text: str
    author: str | None = None
    likes: int | None = Field(default=None, ge=0)
    reply_count: int | None = Field(default=None, ge=0)
    created_at: str | None = None
    video_url: str | None = None
    platform: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    metric_notes: dict[str, str] = Field(default_factory=dict)
    source_record_id: str
    snapshot_hash: str

    def expected_hash(self) -> str:
        import json
        data = self.model_dump(exclude={'source_record_id', 'snapshot_hash'})
        return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

    @model_validator(mode='after')
    def check_hash(self) -> SignalSource:
        if self.snapshot_hash != self.expected_hash():
            raise ValueError('source snapshot hash mismatch')
        identity = f"{self.platform or ''}\x00{self.video_url or ''}\x00{self.comment_id}"
        expected_id = 'source-' + hashlib.sha256(identity.encode()).hexdigest()
        if self.source_record_id != expected_id:
            raise ValueError('source ID mismatch')
        return self

def validate_source_span(source: SignalSource, source_record_id: str, snapshot_hash: str, start: int, end: int, evidence_quote: str) -> None:
    """Shared persisted-claim provenance check for signals and customer context."""
    if source_record_id != source.source_record_id or snapshot_hash != source.snapshot_hash:
        raise ValueError('broken source reference')
    if not 0 <= start < end <= len(source.text):
        raise ValueError('invalid source span')
    if source.text[start:end] != evidence_quote:
        raise ValueError('quote does not match source span')

ContextField = Literal['audience_segment', 'context', 'situation', 'life_or_business_stage', 'user_buyer_distinction']

def artifact_hash(model: StrictModel) -> str:
    return hashlib.sha256(json.dumps(model.model_dump(mode='json'), ensure_ascii=False, sort_keys=True).encode()).hexdigest()

class EvidenceRef(StrictModel):
    evidence_id: str
    origin: Literal['signal', 'context']
    upstream_claim_id: str
    comment_id: str
    source_record_id: str
    source_hash: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    evidence_quote: str
    signal_path: str
    truth_type: TruthType

class Support(StrictModel):
    comment_count: int = Field(ge=0)
    unique_authors: int | None = Field(default=None, ge=0)
    known_author_count: int = Field(ge=0)
    unknown_author_comments: int = Field(ge=0)
    source_count: int | None = Field(default=None, ge=0)
    known_source_count: int = Field(ge=0)
    unknown_source_comments: int = Field(ge=0)
    total_likes: int | None = Field(default=None, ge=0)
    known_likes_sum: int = Field(ge=0)
    unknown_likes_comments: int = Field(ge=0)
    total_replies: int | None = Field(default=None, ge=0)
    known_replies_sum: int = Field(ge=0)
    unknown_replies_comments: int = Field(ge=0)

class Variation(StrictModel):
    label: str
    truth_type: Literal['DERIVED'] = 'DERIVED'
    evidence_refs: list[EvidenceRef]

class ContextVariant(Variation):
    field: ContextField
    support: Support

class CounterEvidence(StrictModel):
    supporting_ref: EvidenceRef
    counter_ref: EvidenceRef
    truth_type: Literal['DERIVED'] = 'DERIVED'
    status: Literal['possible_contradiction'] = 'possible_contradiction'

class CustomerProfileLinks(StrictModel):
    jobs: list[str] = Field(default_factory=list)
    pains: list[str] = Field(default_factory=list)
    gains: list[str] = Field(default_factory=list)
    behavior: list[str] = Field(default_factory=list)
    language: list[str] = Field(default_factory=list)
    context: list[str] = Field(default_factory=list)

class InsightScope(StrictModel):
    population: Literal['cited_source_comments_only'] = 'cited_source_comments_only'
    relationship_scope: Literal['within_comments', 'across_corpus']
    source_comment_ids: list[str]
    shared_comment_ids: list[str]
    audience_segment: list[ContextVariant] = Field(default_factory=list)
    context: list[ContextVariant] = Field(default_factory=list)
    situation: list[ContextVariant] = Field(default_factory=list)
    life_or_business_stage: list[ContextVariant] = Field(default_factory=list)
    user_buyer_distinction: list[ContextVariant] = Field(default_factory=list)
    missing_context_comments: list[str]

class EvidenceBundle(StrictModel):
    customer_profile_links: CustomerProfileLinks
    scope: InsightScope
    evidence_summary: Support
    evidence_refs: list[EvidenceRef]
    variations: list[Variation]
    contradictions: list[CounterEvidence]
    evidence_kind: list[Literal['customer_speech']]
    limitations: list[str]

Assessment = Literal['high', 'medium', 'low', 'unknown']

class PriorityDecision(StrictModel):
    priority_status: Literal['unassessed', 'monitor', 'priority_need'] = 'unassessed'
    assessment_origin: Literal['human_assessment'] = 'human_assessment'
    important: Assessment = 'unknown'
    urgent: Assessment = 'unknown'
    frequent: Assessment = 'unknown'
    expensive: Assessment = 'unknown'
    emotional_intensity: Assessment = 'unknown'
    note: str = Field(default='', max_length=8000)

class VerifiedStatement(StrictModel):
    text: str
    truth_type: Literal['DERIVED'] = 'DERIVED'
    statement_origin: Literal['machine_approved', 'human_edited']

class HumanVerification(StrictModel):
    source_grounded: Literal[True] = True
    evidence_support_present: Literal[True] = True
    machine_review_passed: Literal[True] = True
    machine_review_scope: Literal['source_candidate_only'] = 'source_candidate_only'
    human_verified: Literal[True] = True
    market_validated: Literal[False] = False
    purchase_validated: Literal[False] = False

class HumanReview(StrictModel):
    review_event_id: str
    reviewer_id: str
    reviewed_at: datetime
    decision: Literal['approved', 'edited_and_approved']
    rationale: str

class VerifiedInsight(EvidenceBundle):
    verified_insight_id: str
    source_candidate_id: str
    source_candidate_hash: str
    source_insights_hash: str
    revision: int = Field(ge=1)
    supersedes: str | None
    statement: VerifiedStatement
    support_pattern_ids: list[str]
    relationship_type: str
    verification: HumanVerification = Field(default_factory=HumanVerification)
    human_review: HumanReview
    priority: PriorityDecision
    status: Literal['verified'] = 'verified'

Purpose = Literal['educate', 'diagnose', 'reframe', 'answer_question', 'handle_objection', 'show_process', 'show_mistake', 'show_tradeoff', 'decision_support', 'story', 'social_proof', 'other']

AngleType = Literal['contrarian', 'diagnostic', 'how_to', 'mistake', 'myth_busting', 'question_answer', 'decision_framework', 'story', 'comparison', 'checklist', 'warning', 'case_lens', 'other']

class ProposedText(StrictModel):
    text: str = Field(min_length=1, max_length=600)
    claim_kind: Literal['general_explanatory', 'creative_framing']
    truth_type: Literal['PROPOSED'] = 'PROPOSED'
    needs_external_evidence: Literal[True] = True

class GroundedScene(StrictModel):
    kind: Literal['source_wording'] = 'source_wording'
    text: str
    truth_type: Literal['OBSERVED', 'DERIVED']
    evidence_ref: EvidenceRef

class ProposedScene(StrictModel):
    kind: Literal['proposed_framing'] = 'proposed_framing'
    framing: ProposedText

class ValueScene(StrictModel):
    truth_type: Literal['PROPOSED'] = 'PROPOSED'
    need_moment: GroundedScene | ProposedScene | None = None
    current_struggle: GroundedScene | ProposedScene | None = None
    desired_future: GroundedScene | ProposedScene | None = None

class SelectedAngle(StrictModel):
    angle_id: str
    angle_hash: str
    tree_hash: str
    project_id: str
    run_id: str
    verified_insight_id: str
    topic_id: str
    content_opportunity_id: str
    selection_event_id: str
    reviewer_id: str
    selected_at: datetime
    selection_rationale: str
    truth_type: Literal['PROPOSED'] = 'PROPOSED'
    status: Literal['selected'] = 'selected'

class PacketProject(StrictModel):
    project_id: str
    project_goal: Literal['CONTENT', 'BOTH'] = 'CONTENT'
    research_run_id: str
    source_route_context: list[str]

class LanguageBank(StrictModel):
    exact_phrases: list[EvidenceRef]
    emotional_wording: list[EvidenceRef]
    repeated_expressions: list[EvidenceRef]
    repetition_scope: Literal['within_source_comment_not_corpus_frequency'] = 'within_source_comment_not_corpus_frequency'

class CustomerTruthZone(StrictModel):
    zone: Literal['A_CUSTOMER_TRUTH'] = 'A_CUSTOMER_TRUTH'
    immutable: Literal[True] = True
    verified_insight: VerifiedInsight
    language_bank: LanguageBank
    representative_quotes: list[EvidenceRef]
    source_snapshots: list[SignalSource]

class PacketOpportunity(StrictModel):
    content_opportunity_id: str
    statement: ProposedText
    purpose: Purpose
    customer_value: ProposedText
    truth_type: Literal['PROPOSED'] = 'PROPOSED'

class PacketTopic(StrictModel):
    topic_id: str
    title: ProposedText
    description: ProposedText
    customer_value: ProposedText
    truth_type: Literal['PROPOSED'] = 'PROPOSED'

class PacketAngle(StrictModel):
    angle_id: str
    title: ProposedText
    angle_type: AngleType
    core_argument: ProposedText
    belief_before: ProposedText
    belief_after: ProposedText
    opening_direction: ProposedText
    customer_value: ProposedText
    truth_type: Literal['PROPOSED'] = 'PROPOSED'

class StrategyZone(StrictModel):
    zone: Literal['B_SELECTED_STRATEGY'] = 'B_SELECTED_STRATEGY'
    truth_type: Literal['PROPOSED'] = 'PROPOSED'
    opportunity: PacketOpportunity
    topic: PacketTopic
    angle: PacketAngle
    value_scene: ValueScene
    content_objective: ProposedText | None

class WriterMay(StrictModel):
    create_hooks: Literal[True] = True
    create_titles: Literal[True] = True
    create_structure: Literal[True] = True
    create_analogies: Literal[True] = True
    create_metaphors: Literal[True] = True
    create_clearly_labeled_illustrative_examples: Literal[True] = True
    choose_storytelling_format: Literal[True] = True
    adapt_brand_voice: Literal[True] = True
    improve_clarity: Literal[True] = True
    generate_cta: Literal[True] = True

class CreativeConstraints(StrictModel):
    no_fake_statistics: Literal[True] = True
    no_fake_case_studies: Literal[True] = True
    no_fake_customers: Literal[True] = True
    no_fake_quotes: Literal[True] = True
    no_fake_demographics: Literal[True] = True
    no_fake_research: Literal[True] = True
    preserve_customer_language: Literal[True] = True
    do_not_change_customer_truth: Literal[True] = True
    external_claims_require_evidence: Literal[True] = True
    no_evidence_level_upgrade: Literal[True] = True
    no_market_validation_claim: Literal[True] = True
    no_purchase_validation_claim: Literal[True] = True
    preserve_contradictions_and_limitations: Literal[True] = True

class ExecutionZone(StrictModel):
    zone: Literal['C_CREATIVE_EXECUTION'] = 'C_CREATIVE_EXECUTION'
    status: Literal['not_generated'] = 'not_generated'
    writer_may: WriterMay = Field(default_factory=WriterMay)
    constraints: CreativeConstraints = Field(default_factory=CreativeConstraints)

class ExternalRequirement(StrictModel):
    strategy_field: str
    claim_needed: str
    purpose: Literal['verify_proposed_framing_before_publication'] = 'verify_proposed_framing_before_publication'
    status: Literal['required_before_publish'] = 'required_before_publish'

class PacketLineage(StrictModel):
    verified_insight_id: str
    source_candidate_id: str
    pattern_ids: list[str]
    comment_ids: list[str]
    source_hashes: list[str]
    content_opportunity_id: str
    topic_id: str
    angle_id: str
    governance_hash: str
    verified_artifact_hash: str
    selection_hash: str
    selected_artifact_hash: str
    content_tree_hash: str
    verified_insight_hash: str
    opportunity_hash: str
    topic_hash: str
    angle_hash: str

class ContentIntelligencePacket(StrictModel):
    schema_version: Literal['v2.content-intelligence-packet.1']
    packet_id: str = Field(pattern='^CIP-[0-9a-f]{64}$')
    packet_revision: int = Field(ge=1, strict=True)
    supersedes_packet_id: str | None = Field(default=None, pattern='^CIP-[0-9a-f]{64}$')
    created_at: datetime
    producer: Literal['customer-intelligence:content-packet.1'] = 'customer-intelligence:content-packet.1'
    project: PacketProject
    customer_truth: CustomerTruthZone
    content_strategy: StrategyZone
    creative_execution: ExecutionZone = Field(default_factory=ExecutionZone)
    external_evidence_requirements: list[ExternalRequirement]
    selection: SelectedAngle
    lineage: PacketLineage

    @model_validator(mode='after')
    def snapshot_integrity(self):
        validate_snapshot(self)
        return self

def value_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def evidence_refs(value):
    """Walk only the selected verified insight, including counter/context references."""
    if isinstance(value, dict):
        if 'evidence_id' in value and 'upstream_claim_id' in value:
            yield EvidenceRef.model_validate(value)
        else:
            for child in value.values():
                yield from evidence_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from evidence_refs(child)

def language_for(vi):
    return LanguageBank(**{key: [r for r in vi.evidence_refs if r.signal_path == 'language.' + key] for key in ('exact_phrases', 'emotional_wording', 'repeated_expressions')})

def representatives(vi):
    result, seen = ([], set())
    for ref in vi.evidence_refs:
        if ref.source_record_id not in seen:
            result.append(ref)
            seen.add(ref.source_record_id)
        if len(result) == 5:
            break
    return result

def external_requirements(strategy):

    def walk(value, path):
        if isinstance(value, dict):
            if value.get('needs_external_evidence') is True and 'text' in value:
                yield ExternalRequirement(strategy_field=path, claim_needed=value['text'])
            else:
                for k, v in value.items():
                    yield from walk(v, path + '.' + k)
    return list(walk(strategy.model_dump(mode='json'), 'content_strategy'))

def packet_identity(data):
    return 'CIP-' + value_hash({k: v for k, v in data.items() if k != 'packet_id'})

def validate_snapshot(packet):
    if packet.created_at.tzinfo is None:
        raise ValueError('packet_time_requires_timezone')
    if (packet.packet_revision == 1) != (packet.supersedes_packet_id is None):
        raise ValueError('invalid_packet_revision')
    if packet.packet_id == packet.supersedes_packet_id:
        raise ValueError('packet_cannot_supersede_itself')
    if packet.packet_id != packet_identity(packet.model_dump(mode='json')):
        raise ValueError('packet_content_hash_mismatch')
    truth, strategy, lineage, selection = (packet.customer_truth, packet.content_strategy, packet.lineage, packet.selection)
    vi = truth.verified_insight
    if lineage.verified_insight_hash != artifact_hash(vi):
        raise ValueError('verified_insight_hash_mismatch')
    if lineage.source_candidate_id != vi.source_candidate_id or lineage.pattern_ids != vi.support_pattern_ids:
        raise ValueError('invalid_customer_lineage')
    if not lineage.verified_insight_id == vi.verified_insight_id == selection.verified_insight_id:
        raise ValueError('insight_lineage_mismatch')
    if not (lineage.angle_id == selection.angle_id == strategy.angle.angle_id and lineage.topic_id == selection.topic_id == strategy.topic.topic_id and (lineage.content_opportunity_id == selection.content_opportunity_id == strategy.opportunity.content_opportunity_id)):
        raise ValueError('strategy_lineage_mismatch')
    if lineage.content_tree_hash != selection.tree_hash or lineage.angle_hash != selection.angle_hash:
        raise ValueError('selection_lineage_mismatch')
    if packet.project.project_id != selection.project_id or packet.project.research_run_id != selection.run_id:
        raise ValueError('project_lineage_mismatch')
    refs = list(evidence_refs(vi.model_dump(mode='json')))
    sources = {s.source_record_id: s for s in truth.source_snapshots}
    if len(sources) != len(truth.source_snapshots) or set(sources) != {r.source_record_id for r in refs}:
        raise ValueError('source_snapshot_set_mismatch')
    for r in refs:
        s = sources[r.source_record_id]
        validate_source_span(s, r.source_record_id, r.source_hash, r.start, r.end, r.evidence_quote)
        if r.comment_id != s.comment_id:
            raise ValueError('comment_id_mismatch')
    if lineage.comment_ids != sorted({r.comment_id for r in refs}) or lineage.source_hashes != sorted({s.snapshot_hash for s in sources.values()}):
        raise ValueError('source_lineage_mismatch')
    if packet.project.source_route_context != sorted({s.platform for s in sources.values() if s.platform}):
        raise ValueError('invented_source_route')
    if truth.language_bank != language_for(vi) or truth.representative_quotes != representatives(vi):
        raise ValueError('unsupported_customer_language_or_quote')
    if packet.external_evidence_requirements != external_requirements(strategy):
        raise ValueError('external_requirements_mismatch')
    for name in ('need_moment', 'current_struggle', 'desired_future'):
        scene = getattr(strategy.value_scene, name)
        if isinstance(scene, GroundedScene):
            r = scene.evidence_ref
            if r not in vi.evidence_refs or scene.text != r.evidence_quote or scene.truth_type != r.truth_type:
                raise ValueError('unsupported_value_scene')
            roles = {'need_moment': ('context.', 'behavior.trigger'), 'current_struggle': ('pains.', 'behavior.'), 'desired_future': ('gains.',)}
            if not r.signal_path.startswith(roles[name]):
                raise ValueError('unsupported_value_scene_role')
    return packet

def validate_revision(packet, previous):
    packet = ContentIntelligencePacket.model_validate(packet.model_dump())
    previous = ContentIntelligencePacket.model_validate(previous.model_dump())
    if packet.supersedes_packet_id != previous.packet_id or packet.packet_revision != previous.packet_revision + 1:
        raise ValueError('broken_packet_revision_chain')
    if (packet.project.project_id, packet.project.research_run_id) != (previous.project.project_id, previous.project.research_run_id):
        raise ValueError('unrelated_packet_revision')
    return packet
