"""Explicitly synthetic human approval fixtures; never owner approval."""
from integrations.content_intelligence.creative_plan import PlanStore
from pathlib import Path
import hashlib


def proposal(packet, library):
    refs = [packet['customer_truth']['verified_insight']['evidence_refs'][0]['evidence_id']]
    def candidate(i, text):
        return dict(candidate_id=i,text=text,rationale='SYNTHETIC expression only',evidence_refs=refs,
                    intent_preserved=True,factual_claims_supported=True,natural_and_meaningful=True)
    return dict(packet_id=packet['packet_id'], verified_insight_id=packet['customer_truth']['verified_insight']['verified_insight_id'],
        angle_id=packet['content_strategy']['angle']['angle_id'], truth_type='PROPOSED', story_matches=[], knowledge_matches=[],
        illustrations=[], psychology=dict(primary_mechanism='Synthetic mechanism', optional_secondary_mechanism=None,
            library_source=library.as_posix(), rationale='SYNTHETIC mechanism, no hidden motive'),
        format='Reel', treatment_or_truc='Selected direction',
        hook_candidates=[candidate('h1','SYNTHETIC draft'),candidate('h2','SYNTHETIC alternative')],
        title_candidates=[candidate('t1','Synthetic'),candidate('t2','Synthetic alternative')],
        recommended_hook_id='h1', recommended_title_id='t1', outline=['SYNTHETIC outline'],
        reader_value=['SYNTHETIC useful distinction'], narrative_payoffs=[],
        reader_value_clear=True, narrative_payoff_clear=True,
        cta_direction='No sale',creative_constraints=['No new customer truth'],truth_preserved=True,
        selected_intent_preserved=True,reader_centered_pov=True,non_prescriptive_tone=True,issues=[])


def approved_fixture(packet, path):
    library=path/'nguyen-ly-tam-ly.md'; library.write_text('Synthetic mechanism',encoding='utf8')
    assets=[dict(path=library.as_posix(),sha256=hashlib.sha256(library.read_bytes()).hexdigest())]
    context=dict(schema_version='reelo.execution-context.1',packet=packet)
    store=PlanStore(path/'creative-plans.sqlite')
    plan=store.save(proposal(packet,library),context,assets,'SYNTHETIC-PLANNER')
    a=store.review(plan['creative_plan_id'],dict(decision='approved',reviewer='SYNTHETIC TEST fixture',
        human_attested=True,approval_kind='synthetic_fixture',expected_plan_hash=plan['plan_hash']))
    return a,assets,store
