import numpy as np
from scipy.stats import norm


def ab_test(df):

    variants = df["variant"].unique()

    if len(variants) != 2:
        return None

    control = df[df["variant"] == variants[0]]
    treatment = df[df["variant"] == variants[1]]

    n1 = len(control)
    n2 = len(treatment)

    c1 = control["conversion"].sum()
    c2 = treatment["conversion"].sum()

    p1 = c1 / n1
    p2 = c2 / n2

    pooled = (c1 + c2) / (n1 + n2)

    se = np.sqrt(
        pooled *
        (1 - pooled) *
        (1 / n1 + 1 / n2)
    )

    z = (p2 - p1) / se

    p_value = 2 * (1 - norm.cdf(abs(z)))

    lift = ((p2 - p1) / p1) * 100

    ci = 1.96 * se

    return {
        "control_rate": p1 * 100,
        "treatment_rate": p2 * 100,
        "lift": lift,
        "z_score": z,
        "p_value": p_value,
        "confidence_low": (p2 - p1 - ci) * 100,
        "confidence_high": (p2 - p1 + ci) * 100,
        "winner": variants[1] if p_value < 0.05 and p2 > p1 else variants[0]
    }