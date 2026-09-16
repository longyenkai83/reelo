"""Small local campaign contract; stages describe strategy, never customer facts."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from integrations.content_intelligence.context_packs import validate_recipe

Stage = Literal['UNAWARE', 'PROBLEM_AWARE', 'SOLUTION_AWARE', 'PRODUCT_AWARE', 'MOST_AWARE']
STAGES = ('UNAWARE', 'PROBLEM_AWARE', 'SOLUTION_AWARE', 'PRODUCT_AWARE', 'MOST_AWARE')
Route = Literal['STORY_LED', 'INSIGHT_LED', 'KNOWLEDGE_POV_LED', 'AUTO_DISCOVERY']
SourceKind = Literal['CUSTOMER_VOICE', 'VERIFIED_INSIGHT', 'CREATOR_STORY', 'CLIENT_STORY',
                     'CREATOR_KNOWLEDGE_POV', 'CREATOR_EXPERIENCE', 'MARKET_OBSERVATION',
                     'FUTURE_POSSIBILITY', 'OFFER_BUSINESS_CONTEXT', 'EXTERNAL_KNOWLEDGE']
CTA = Literal['REFLECT', 'ENGAGE', 'SAVE_FOLLOW', 'GET_RESOURCE', 'LEARN_METHOD', 'ASK_DM',
              'EXPLORE_OFFER', 'BOOK_BUY_APPLY']
COMMERCIAL = {'EXPLORE_OFFER', 'BOOK_BUY_APPLY'}
EARLY = {'UNAWARE', 'PROBLEM_AWARE'}


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Source(Model):
    source_id: str = Field(min_length=1)
    creator_id: str = Field(min_length=1)
    kind: SourceKind
    path: str
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    section: str = Field(min_length=1)
    summary: str = Field(min_length=1)  # Index/proposal only, not evidence.
    topics: list[str] = Field(min_length=1)
    provenance: str = Field(min_length=1)
    truth_type: Literal['OBSERVED', 'DERIVED', 'HYPOTHESIS', 'PROPOSED']
    permission_ref: str | None = None
    permission_sha256: str | None = None
    packet_id: str | None = None

    @model_validator(mode='after')
    def truth_boundary(self):
        if self.kind == 'FUTURE_POSSIBILITY' and self.truth_type not in ('PROPOSED', 'HYPOTHESIS'):
            raise ValueError('future_possibility_is_not_observed')
        if self.kind == 'VERIFIED_INSIGHT' and (not self.packet_id or self.truth_type != 'DERIVED'):
            raise ValueError('verified_insight_requires_actual_packet')
        if self.kind != 'VERIFIED_INSIGHT' and self.packet_id is not None:
            raise ValueError('non_insight_must_not_claim_packet_identity')
        return self


class SourceUse(Model):
    source_id: str
    contribution: str = Field(min_length=1)


class Offer(Model):
    source_id: str
    intended_next_step: str = Field(min_length=1)


class CampaignRequest(Model):
    campaign_id: str = Field(min_length=1, pattern=r'^[A-Za-z0-9_-]+$')
    creator_id: str = Field(min_length=1)
    campaign_goal: str = Field(min_length=1)
    audience_scope: str = Field(min_length=1)
    starting_awareness_stage: Stage
    target_awareness_stage: Stage
    content_count: int = Field(ge=1, le=100)
    autonomy_mode: Literal['GUIDED', 'AUTOPILOT']
    route: Route
    topics: list[str] = Field(min_length=1)
    timing: str = Field(min_length=1)
    offer_context: Offer | None = None
    resource_source_id: str | None = None
    allowed_cta_intents: list[CTA] = Field(min_length=1)
    modes: list[Literal['REEL', 'SHORT_ARTICLE', 'LONG_ARTICLE']] = Field(min_length=1)
    boundaries: list[str] = Field(min_length=1)


class Slot(Model):
    slot_id: str
    order: int = Field(ge=1)
    journey_stage: Stage
    journey_objective: str = Field(min_length=1)
    movement: Literal['MOVE', 'REINFORCE']
    next_intended_stage: Stage
    one_idea: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    content_job: str
    recipe_id: str
    primary_source: SourceUse
    supporting_sources: list[SourceUse] = Field(default_factory=list, max_length=2)
    reader_value: str = Field(min_length=1)
    cta_intent: CTA
    mode: Literal['REEL', 'SHORT_ARTICLE', 'LONG_ARTICLE']
    dependencies: list[str]
    status: Literal['PROPOSED'] = 'PROPOSED'

    @model_validator(mode='after')
    def coherent(self):
        validate_recipe(self.content_job, self.recipe_id)
        ids = [self.primary_source.source_id] + [s.source_id for s in self.supporting_sources]
        if len(set(ids)) != len(ids): raise ValueError('duplicate_source_role')
        if self.journey_stage in EARLY and self.cta_intent in COMMERCIAL:
            raise ValueError('early_stage_commercial_cta')
        if self.cta_intent == 'BOOK_BUY_APPLY' and self.journey_stage != 'MOST_AWARE':
            raise ValueError('direct_sale_requires_selling_stage')
        if self.cta_intent == 'EXPLORE_OFFER' and self.journey_stage not in ('PRODUCT_AWARE', 'MOST_AWARE'):
            raise ValueError('offer_requires_product_context')
        if (self.movement == 'REINFORCE') != (self.journey_stage == self.next_intended_stage):
            raise ValueError('journey_movement_mismatch')
        return self


class JourneyPlan(Model):
    schema_version: Literal['reelo.journey-plan.1'] = 'reelo.journey-plan.1'
    request: CampaignRequest
    sources: list[Source] = Field(min_length=1)
    sequence: list[Slot] = Field(min_length=1)
    editorial_history: list[dict] = Field(default_factory=list)  # Context, never customer evidence/approval.
    strategy_truth_type: Literal['PROPOSED'] = 'PROPOSED'
    audience_state_is_observed: Literal[False] = False

    @model_validator(mode='after')
    def coherent(self):
        r = self.request
        if len(self.sequence) != r.content_count: raise ValueError('campaign_count_mismatch')
        by_id = {s.source_id: s for s in self.sources}
        if len(by_id) != len(self.sources): raise ValueError('duplicate_source_identity')
        if any(s.creator_id != r.creator_id for s in self.sources): raise ValueError('creator_scope_mismatch')
        previous = []
        current = r.starting_awareness_stage
        for n, slot in enumerate(self.sequence, 1):
            if slot.order != n or slot.slot_id in previous or slot.dependencies != previous:
                raise ValueError('sequence_dependencies_invalid')
            if slot.journey_stage != current: raise ValueError('journey_sequence_discontinuity')
            current = slot.next_intended_stage
            if slot.mode not in r.modes or slot.cta_intent not in r.allowed_cta_intents:
                raise ValueError('slot_outside_campaign_scope')
            if slot.topic not in r.topics: raise ValueError('topic_outside_scope')
            for use in [slot.primary_source, *slot.supporting_sources]:
                if use.source_id not in by_id: raise ValueError('unknown_source')
                if slot.topic not in by_id[use.source_id].topics: raise ValueError('source_topic_mismatch')
            primary = by_id[slot.primary_source.source_id]
            permitted = {'STORY_LED': {'CREATOR_STORY', 'CREATOR_EXPERIENCE', 'CLIENT_STORY'},
                'INSIGHT_LED': {'VERIFIED_INSIGHT'},
                'KNOWLEDGE_POV_LED': {'CREATOR_KNOWLEDGE_POV', 'EXTERNAL_KNOWLEDGE', 'MARKET_OBSERVATION', 'FUTURE_POSSIBILITY'},
                'AUTO_DISCOVERY': set()}
            if permitted[r.route] and primary.kind not in permitted[r.route]:
                raise ValueError('entry_route_primary_mismatch')
            if slot.cta_intent in COMMERCIAL and r.offer_context is None:
                raise ValueError('commercial_cta_requires_offer')
            selected_ids = {u.source_id for u in [slot.primary_source, *slot.supporting_sources]}
            if slot.cta_intent in COMMERCIAL and r.offer_context.source_id not in selected_ids:
                raise ValueError('offer_must_count_as_selected_source')
            if slot.cta_intent == 'GET_RESOURCE' and (r.resource_source_id not in by_id or
                    by_id[r.resource_source_id].kind != 'OFFER_BUSINESS_CONTEXT'):
                raise ValueError('resource_cta_requires_real_resource')
            if slot.cta_intent == 'GET_RESOURCE' and r.resource_source_id not in selected_ids:
                raise ValueError('resource_must_count_as_selected_source')
            previous.append(slot.slot_id)
        if current != r.target_awareness_stage: raise ValueError('target_stage_not_reached_in_plan')
        if r.offer_context and (r.offer_context.source_id not in by_id or
                by_id[r.offer_context.source_id].kind != 'OFFER_BUSINESS_CONTEXT'):
            raise ValueError('offer_source_required')
        return self


# These are ranges of documented meanings, not a conversion of creator records.
LEGACY_CROSSWALK = {
    'cold': dict(stages=['UNAWARE', 'PROBLEM_AWARE'], meaning='recognition, reach; no sales', exact=False),
    'warm': dict(stages=['PROBLEM_AWARE', 'SOLUTION_AWARE'], meaning='trust, education; optional genuine resource', exact=False),
    'hot_pre_purchase': dict(stages=['SOLUTION_AWARE', 'PRODUCT_AWARE'], meaning='category/proof/objections; no direct pitch', exact=False),
    'hot_sale_library': dict(stages=['PRODUCT_AWARE', 'MOST_AWARE'], meaning='creator CTA library groups hot with selling; explicit commercial scope required', exact=False),
    'sell': dict(stages=['MOST_AWARE'], meaning='clear real offer and one direct CTA when authorized', exact=False),
}


def legacy_meaning(label):
    if label in ('hot', 'nong', 'nóng'): raise ValueError('ambiguous_hot_requires_semantic_variant')
    return LEGACY_CROSSWALK[label]
