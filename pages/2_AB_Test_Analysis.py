import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

from utils.loader import load_data
from utils.statistics import ab_test

st.set_page_config(
    page_title="A/B Test Analysis",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 A/B Experiment Analysis")

st.markdown(
    "Evaluate experiment performance using statistical significance testing."
)

df = load_data()

st.write(df["variant"].value_counts())
st.write(df["variant"].unique())

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("Experiment Filters")

device = st.sidebar.multiselect(
    "Device",
    sorted(df["device_type"].unique()),
    default=sorted(df["device_type"].unique())
)

traffic = st.sidebar.multiselect(
    "Traffic Source",
    sorted(df["traffic_source"].unique()),
    default=sorted(df["traffic_source"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

login = st.sidebar.multiselect(
    "Login",
    sorted(df["login_y_n"].unique()),
    default=sorted(df["login_y_n"].unique())
)

returning = st.sidebar.multiselect(
    "Returning User",
    sorted(df["return_y_n"].unique()),
    default=sorted(df["return_y_n"].unique())
)

filtered = df[
    df["device_type"].isin(device)
    &
    df["traffic_source"].isin(traffic)
    &
    df["region"].isin(region)
    &
    df["login_y_n"].isin(login)
    &
    df["return_y_n"].isin(returning)
]

result = ab_test(filtered)

if result is None:
    st.error("Exactly two experiment variants are required.")
    st.stop()

variants = filtered["variant"].unique()

control = filtered[filtered["variant"] == variants[0]]
treatment = filtered[filtered["variant"] == variants[1]]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Control Conversion",
    f"{result['control_rate']:.2f}%"
)

c2.metric(
    "Treatment Conversion",
    f"{result['treatment_rate']:.2f}%"
)

c3.metric(
    "Relative Lift",
    f"{result['lift']:.2f}%"
)

c4.metric(
    "P-value",
    f"{result['p_value']:.5f}"
)

st.divider()

# -------------------------------------------------
# Statistical Summary
# -------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Experiment Statistics")

    st.write(f"**Z Score:** {result['z_score']:.4f}")

    st.write(f"**Confidence Interval Low:** {result['confidence_low']:.2f}%")

    st.write(f"**Confidence Interval High:** {result['confidence_high']:.2f}%")

    if result["p_value"] < 0.05:
        st.success("Result is statistically significant.")
    else:
        st.warning("Result is NOT statistically significant.")

with right:

    summary = {
        "Metric": [
            "Control Users",
            "Treatment Users",
            "Control Conversions",
            "Treatment Conversions"
        ],
        "Value": [
            len(control),
            len(treatment),
            control["conversion"].sum(),
            treatment["conversion"].sum()
        ]
    }

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------
# Conversion Comparison
# -------------------------------------------------

compare = {
    "Variant": [
        variants[0],
        variants[1]
    ],
    "Conversion Rate": [
        result["control_rate"],
        result["treatment_rate"]
    ]
}

fig = px.bar(
    compare,
    x="Variant",
    y="Conversion Rate",
    text="Conversion Rate",
    color="Variant",
    title="Conversion Rate Comparison"
)

fig.update_traces(
    texttemplate="%{text:.2f}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Conversion Funnel
# -------------------------------------------------

funnel = {
    "Stage": [
        "Visitors",
        "Conversions"
    ],
    variants[0]: [
        len(control),
        control["conversion"].sum()
    ],
    variants[1]: [
        len(treatment),
        treatment["conversion"].sum()
    ]
}

fig = go.Figure()

fig.add_trace(
    go.Funnel(
        name=variants[0],
        y=funnel["Stage"],
        x=funnel[variants[0]]
    )
)

fig.add_trace(
    go.Funnel(
        name=variants[1],
        y=funnel["Stage"],
        x=funnel[variants[1]]
    )
)

fig.update_layout(
    title="Conversion Funnel"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Daily Experiment Trend
# -------------------------------------------------

daily = (
    filtered
    .groupby(["date", "variant"])
    .agg(
        Conversion=("conversion", "mean")
    )
    .reset_index()
)

daily["Conversion"] *= 100

fig = px.line(
    daily,
    x="date",
    y="Conversion",
    color="variant",
    title="Daily Conversion Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Confidence Interval
# -------------------------------------------------

ci = go.Figure()

ci.add_trace(
    go.Scatter(
        x=[
            result["confidence_low"],
            result["confidence_high"]
        ],
        y=["Difference", "Difference"],
        mode="lines+markers",
        name="95% CI"
    )
)

ci.update_layout(
    title="95% Confidence Interval",
    xaxis_title="Conversion Difference (%)"
)

st.plotly_chart(
    ci,
    use_container_width=True
)

# -------------------------------------------------
# Normal Distribution
# -------------------------------------------------

x = [i / 100 for i in range(-400, 401)]

y = [norm.pdf(v) for v in x]

dist = go.Figure()

dist.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name="Normal Distribution"
    )
)

dist.add_vline(
    x=result["z_score"] / 100,
    line_dash="dash",
    annotation_text="Observed Z"
)

dist.update_layout(
    title="Z-Test Distribution"
)

st.plotly_chart(
    dist,
    use_container_width=True
)

# -------------------------------------------------
# Decision Engine
# -------------------------------------------------

st.subheader("Decision Recommendation")

if result["p_value"] < 0.05:

    if result["treatment_rate"] > result["control_rate"]:

        st.success(
            f"""
### Deploy **{variants[1]}**

Reason

• Statistically Significant

• Higher Conversion

• Lift = {result['lift']:.2f}%

• P-value = {result['p_value']:.5f}
"""
        )

    else:

        st.info(
            f"""
### Keep **{variants[0]}**

Treatment underperformed.

No deployment recommended.
"""
        )

else:

    st.warning(
        """
Experiment is inconclusive.

Recommendation:

• Continue experiment

• Increase sample size

• Re-run significance test
"""
    )

# -------------------------------------------------
# Raw Variant Summary
# -------------------------------------------------

summary = (
    filtered
    .groupby("variant")
    .agg(
        Users=("conversion", "count"),
        Conversions=("conversion", "sum"),
        Conversion_Rate=("conversion", "mean")
    )
    .reset_index()
)

summary["Conversion_Rate"] *= 100

st.subheader("Variant Summary")

st.dataframe(
    summary,
    use_container_width=True
)

# -------------------------------------------------
# Export
# -------------------------------------------------

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Experiment Summary",
    csv,
    "ab_test_summary.csv",
    "text/csv"
)