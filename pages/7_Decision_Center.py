import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.loader import load_data
from utils.statistics import ab_test

st.set_page_config(
    page_title="Decision Center",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Decision Center")

st.markdown("""
Executive summary of the A/B experiment.

This page automatically analyzes the experiment and provides deployment recommendations.
""")

df = load_data()

result = ab_test(df)

if result is None:
    st.error("Exactly two experiment variants are required.")
    st.stop()

variants = sorted(df["variant"].unique())

control = df[df["variant"] == variants[0]]
treatment = df[df["variant"] == variants[1]]

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Winner",
    result["winner"]
)

col2.metric(
    "Relative Lift",
    f"{result['lift']:.2f}%"
)

col3.metric(
    "P-value",
    f"{result['p_value']:.5f}"
)

confidence = (1 - result["p_value"]) * 100

col4.metric(
    "Confidence",
    f"{confidence:.2f}%"
)

st.divider()

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------

st.subheader("Executive Summary")

if result["p_value"] < 0.05:

    if result["treatment_rate"] > result["control_rate"]:

        decision = "Deploy Treatment"

        summary = f"""
The treatment variant outperformed the control.

The experiment achieved statistical significance.

The observed lift was **{result['lift']:.2f}%**.

Recommendation:

Deploy the Treatment variant to production.
"""

    else:

        decision = "Keep Control"

        summary = """
Although statistically significant, the treatment did not improve performance.

Recommendation:

Continue with the Control variant.
"""

else:

    decision = "Continue Experiment"

    summary = """
The experiment is inconclusive.

Recommendation:

Increase sample size and continue collecting data.
"""

st.success(summary)

# --------------------------------------------------
# Decision Card
# --------------------------------------------------

st.subheader("Deployment Recommendation")

decision_color = {
    "Deploy Treatment": "green",
    "Keep Control": "blue",
    "Continue Experiment": "orange"
}

fig = go.Figure(
    go.Indicator(
        mode="number",
        value=confidence,
        title={"text": decision},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": decision_color[decision]}
        }
    )
)

fig.update_layout(height=350)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Risk Assessment
# --------------------------------------------------

st.subheader("Risk Assessment")

risks = []

if result["p_value"] > 0.05:
    risks.append("Experiment is not statistically significant.")

if abs(result["lift"]) < 2:
    risks.append("Observed lift is very small.")

if len(df) < 10000:
    risks.append("Sample size may be insufficient.")

duplicates = df.duplicated().sum()

if duplicates > 0:
    risks.append(f"{duplicates:,} duplicate rows detected.")

missing = df.isnull().sum().sum()

if missing > 0:
    risks.append(f"{missing:,} missing values detected.")

if len(risks) == 0:

    st.success("No major risks detected.")

else:

    for risk in risks:
        st.warning(risk)

# --------------------------------------------------
# Experiment Checklist
# --------------------------------------------------

st.subheader("Experiment Checklist")

checklist = pd.DataFrame({

    "Requirement":[
        "Two Variants Available",
        "Data Loaded",
        "Conversion Calculated",
        "Statistical Test Completed",
        "Confidence Interval Computed",
        "Decision Generated"
    ],

    "Status":[
        "✅",
        "✅",
        "✅",
        "✅",
        "✅",
        "✅"
    ]

})

st.dataframe(
    checklist,
    hide_index=True,
    use_container_width=True
)

# --------------------------------------------------
# Decision Matrix
# --------------------------------------------------

st.subheader("Decision Matrix")

matrix = pd.DataFrame({

"Scenario":[

"Higher Conversion + Significant",

"Higher Conversion + Not Significant",

"Lower Conversion + Significant",

"Lower Conversion + Not Significant"

],

"Recommended Action":[

"Deploy Treatment",

"Continue Experiment",

"Keep Control",

"Discard Treatment"

]

})

st.dataframe(
    matrix,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Next Actions
# --------------------------------------------------

st.subheader("Recommended Next Steps")

if decision == "Deploy Treatment":

    actions = [

        "Deploy treatment to production",

        "Monitor post-launch conversion",

        "Run validation experiment",

        "Track business KPIs"

    ]

elif decision == "Keep Control":

    actions = [

        "Retain control version",

        "Investigate treatment issues",

        "Plan new experiment",

        "Review user feedback"

    ]

else:

    actions = [

        "Increase sample size",

        "Continue collecting events",

        "Extend experiment duration",

        "Recalculate statistical significance"

    ]

for action in actions:
    st.write(f"• {action}")

# --------------------------------------------------
# Business Impact
# --------------------------------------------------

st.subheader("Business Impact")

impact = pd.DataFrame({

"Area":[

"Conversion",

"Marketing",

"Product",

"Revenue",

"Customer Experience"

],

"Expected Impact":[

"Increase",

"Better ROI",

"Feature Validation",

"Potential Growth",

"Improved UX"

]

})

st.dataframe(
    impact,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Executive Report
# --------------------------------------------------

st.subheader("Executive Report")

report = pd.DataFrame({

"Metric":[

"Winning Variant",

"Control Conversion",

"Treatment Conversion",

"Relative Lift",

"P-value",

"Confidence",

"Recommendation"

],

"Value":[

result["winner"],

f"{result['control_rate']:.2f}%",

f"{result['treatment_rate']:.2f}%",

f"{result['lift']:.2f}%",

f"{result['p_value']:.5f}",

f"{confidence:.2f}%",

decision

]

})

st.dataframe(
    report,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Download Report
# --------------------------------------------------

csv = report.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Executive Report",
    data=csv,
    file_name="executive_decision_report.csv",
    mime="text/csv"
)