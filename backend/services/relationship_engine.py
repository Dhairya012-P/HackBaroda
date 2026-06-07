def build_relationships(events):

    relationships = []

    events = sorted(
        events,
        key=lambda x: x.date
    )

    finding = None
    remediation = None
    deadline = None
    regulation = None

    for event in events:

        if event.event_type == "Audit Finding":
            finding = event

        elif event.event_type == "Remediation Assigned":
            remediation = event

        elif event.event_type == "Missed Deadline":
            deadline = event

        elif event.event_type == "Regulation Update":
            regulation = event

    if finding:
        relationships.append(
            "Audit Finding Detected"
        )

    if finding and remediation:
        relationships.append(
            "Remediation Assigned"
        )

    if remediation and deadline:
        relationships.append(
            "Remediation Failed"
        )

    if deadline and regulation:
        relationships.append(
            "Risk Increased Due To New Regulation"
        )

    return relationships