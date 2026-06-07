def generate_analysis(risk):

    return (
        f"This compliance issue has a risk score of "
        f"{risk['score']} and is classified as "
        f"{risk['level']}. "
        f"The primary causes are: "
        f"{', '.join(risk['reasons'])}."
    )