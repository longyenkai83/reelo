"""Synthetic E1 proposal; never an owner decision or generated content."""
from copy import deepcopy
from .creative_fixture import proposal


def purified(packet, library):
    old = proposal(packet, library)
    candidate = deepcopy(old['title_candidates'][1])
    other = deepcopy(candidate); other.update(candidate_id='t3', text='Synthetic third internal option')
    return dict(schema_version='reelo.creative-plan.e1',
        **{k: old[k] for k in ('packet_id', 'verified_insight_id', 'angle_id', 'truth_type',
            'reader_value', 'content_job', 'recipe_id', 'outline', 'cta_direction')},
        format='SHORT_ARTICLE', one_idea='SYNTHETIC selected meaning', payoff='SYNTHETIC useful distinction',
        proof_plan=[dict(kind='CUSTOMER_EVIDENCE', supports='SYNTHETIC source statement', requires_factual_support=True,
                        evidence_ids=old['hook_candidates'][0]['evidence_refs'], contribution='Ground the selected idea')],
        emotional_movement=dict(start_state='Question', tension_or_question='What does the evidence say?',
                                change_or_turn=None, end_state='Clarity'),
        opening_plan=dict(recommended=old['hook_candidates'][0], alternative=None),
        title_plan=dict(recommended=old['title_candidates'][0], alternative=None),
        compatibility_titles=[dict(candidate=c,frame='SELF_MADE') for c in (candidate,other)],
        psychology='NONE', safety={k:old[k] for k in ('truth_preserved','selected_intent_preserved',
            'reader_centered_pov','non_prescriptive_tone','reader_value_clear','narrative_payoff_clear')})
