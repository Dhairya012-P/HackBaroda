def calculate_risk(events):

    score = 0
    reasons = []

    for event in events:

        if event.severity == "High":
            score += 30
            reasons.append("High Severity Finding")

        if event.event_type == "Missed Deadline":
            score += 25
            reasons.append("Missed Deadline")

        if event.status == "Open":
            score += 20
            reasons.append("Open Finding")

        if event.event_type == "Regulation Update":
            score += 25
            reasons.append("New Regulation Impact")

    score = min(score, 100)

    if score >= 81:
        level = "Critical"
    elif score >= 61:
        level = "High"
    elif score >= 31:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": score,
        "level": level,
        "reasons": list(set(reasons))
    }