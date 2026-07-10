import streamlit as st
import plotly.express as px
import pandas as pd

from utils.loader import load_data
from utils.quality import *

st.set_page_config(
    page_title="Data Quality",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Data Quality Dashboard")

st.markdown(
    "Monitor data freshness, completeness and overall health."
)

df = load_data()

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

missing = df.isnull().sum().sum()
duplicates = duplicate_rows(df)
latest = freshness(df)
health = health_score(df)
invalid = invalid_conversions(df)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Rows",
    f"{len(df):,}"
)

c2.metric(
    "Missing Values",
    f"{missing:,}"
)

c3.metric(
    "Duplicate Rows",
    f"{duplicates:,}"
)

c4.metric(
    "Health Score",
    f"{health:.1f}/100"
)

c5.metric(
    "Invalid Conversion",
    invalid
)

st.divider()

# -------------------------------------------------
# Dataset Information
# -------------------------------------------------

st.subheader("Dataset Information")

info = pd.DataFrame({
    "Property":[
        "Rows",
        "Columns",
        "Latest Date",
        "Oldest Date"
    ],
    "Value":[
        len(df),
        len(df.columns),
        str(df["date"].max().date()),
        str(df["date"].min().date())
    ]
})

st.dataframe(
    info,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------
# Missing Values
# -------------------------------------------------

st.subheader("Missing Values")

miss = missing_values(df)

fig = px.bar(
    miss,
    x="Column",
    y="Missing",
    text="Missing",
    title="Missing Values by Column"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Null Percentage
# -------------------------------------------------

st.subheader("Null Percentage")

nulls = null_percentage(df)

fig = px.bar(
    nulls,
    x="Column",
    y="Null %",
    text="Null %",
    color="Null %",
    title="Null Percentage"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Daily Records
# -------------------------------------------------

st.subheader("Daily Record Volume")

daily = daily_records(df)

fig = px.line(
    daily,
    x="date",
    y="Records",
    markers=True,
    title="Daily Records"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Duplicate Check
# -------------------------------------------------

st.subheader("Duplicate Analysis")

duplicate_df = pd.DataFrame({
    "Category":[
        "Unique",
        "Duplicate"
    ],
    "Rows":[
        len(df)-duplicates,
        duplicates
    ]
})

fig = px.pie(
    duplicate_df,
    names="Category",
    values="Rows",
    title="Duplicate Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Conversion Validation
# -------------------------------------------------

st.subheader("Conversion Validation")

conversion_check = pd.DataFrame({
    "Conversion Value":[0,1],
    "Count":[
        len(df[df["conversion"]==0]),
        len(df[df["conversion"]==1])
    ]
})

fig = px.bar(
    conversion_check,
    x="Conversion Value",
    y="Count",
    text="Count",
    title="Conversion Value Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Column Data Types
# -------------------------------------------------

st.subheader("Column Data Types")

dtype = pd.DataFrame({
    "Column":df.columns,
    "Data Type":[str(i) for i in df.dtypes]
})

st.dataframe(
    dtype,
    use_container_width=True
)

# -------------------------------------------------
# Freshness
# -------------------------------------------------

st.subheader("Freshness")

today = pd.Timestamp.today().normalize()

lag = (today - latest.normalize()).days

if lag <= 1:

    st.success(
        f"Dataset is fresh.\n\nLatest data : {latest.date()}"
    )

elif lag <= 7:

    st.warning(
        f"Dataset is {lag} days old."
    )

else:

    st.error(
        f"Dataset is stale ({lag} days old)."
    )

# -------------------------------------------------
# Data Health Gauge
# -------------------------------------------------

fig = px.bar(
    x=["Health Score"],
    y=[health],
    range_y=[0,100],
    text=[round(health,1)],
    title="Overall Data Health"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Validation Checklist
# -------------------------------------------------

st.subheader("Validation Checklist")

checks = pd.DataFrame({
    "Check":[
        "Dataset Loaded",
        "Missing Values Checked",
        "Duplicate Checked",
        "Freshness Verified",
        "Conversion Validated",
        "Data Types Verified"
    ],
    "Status":[
        "✅ Pass",
        "✅ Pass" if missing==0 else "⚠ Review",
        "✅ Pass" if duplicates==0 else "⚠ Review",
        "✅ Pass",
        "✅ Pass" if invalid==0 else "❌ Fail",
        "✅ Pass"
    ]
})

st.dataframe(
    checks,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(
    df.head(100),
    use_container_width=True,
    height=350
)

# -------------------------------------------------
# Export Quality Report
# -------------------------------------------------

report = pd.DataFrame({
    "Metric":[
        "Rows",
        "Missing Values",
        "Duplicates",
        "Health Score",
        "Invalid Conversion",
        "Latest Date"
    ],
    "Value":[
        len(df),
        missing,
        duplicates,
        health,
        invalid,
        latest
    ]
})

csv = report.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Quality Report",
    csv,
    "data_quality_report.csv",
    "text/csv"
)