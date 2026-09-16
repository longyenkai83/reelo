"""Read evidence from a real CIP, or an explicitly distinct journey context."""
def is_journey(context):
    return context.get('schema_version') == 'reelo.journey-context.1'


def evidence(context):
    packet = context.get('packet')
    if packet is None:
        if not is_journey(context): raise ValueError('packet_required')
        return [], []
    insight = packet['customer_truth']['verified_insight']
    return (insight['evidence_refs'] + [c['counter_ref'] for c in insight['contradictions']],
            packet['external_evidence_requirements'])
