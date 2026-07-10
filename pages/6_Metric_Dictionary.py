import streamlit as st
import pandas as pd

from utils.loader import load_data

st.set_page_config(
    page_title="Metric Dictionary",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Metric Dictionary")

st.markdown("""
This page documents every KPI used in the dashboard.

Each metric includes:

- Business Meaning
- Formula
- Source
- Business Decision
""")

df = load_data()

# --------------------------------------------------
# Metric Dictionary
# --------------------------------------------------

dictionary = pd.DataFrame({

"Metric":[

"Total Users",

"Total Conversions",

"Conversion Rate",

"Control Conversion Rate",

"Treatment Conversion Rate",

"Relative Lift",

"Absolute Lift",

"P-value",

"Z Score",

"Confidence Interval",

"Traffic Source Conversion",

"Device Conversion",

"Region Conversion",

"Login Conversion",

"Returning User Conversion",

"Health Score",

"Duplicate Rows",

"Missing Values",

"Freshness",

"Variant Winner"

],

"Formula":[

"COUNT(*)",

"SUM(conversion)",

"Conversions / Users",

"Conversions(Control)/Users(Control)",

"Conversions(Treatment)/Users(Treatment)",

"(Treatment-Control)/Control",

"Treatment-Control",

"Two Proportion Z-Test",

"(Difference/Std Error)",

"95% Statistical Interval",

"AVG(conversion)",

"AVG(conversion)",

"AVG(conversion)",

"AVG(conversion)",

"AVG(conversion)",

"100-(Penalty)",

"Duplicated Rows",

"NULL Count",

"Latest Event Date",

"Higher Statistically Significant Conversion"

],

"Source":[

"Dataset",

"Dataset",

"Dataset",

"Dataset",

"Dataset",

"Calculated",

"Calculated",

"SciPy",

"SciPy",

"SciPy",

"Dataset",

"Dataset",

"Dataset",

"Dataset",

"Dataset",

"Quality Module",

"Quality Module",

"Quality Module",

"Date Column",

"A/B Engine"

],

"Business Decision":[

"Traffic Volume",

"Campaign Success",

"Launch Decision",

"Baseline Performance",

"Treatment Performance",

"Ship Experiment",

"Performance Difference",

"Significance",

"Experiment Confidence",

"Reliability",

"Marketing Budget",

"Device Optimization",

"Regional Targeting",

"Authentication Strategy",

"Retention Strategy",

"Dataset Reliability",

"Data Cleaning",

"Data Validation",

"Pipeline Monitoring",

"Deployment"

]

})

st.dataframe(
    dictionary,
    use_container_width=True,
    height=700
)

# --------------------------------------------------
# Metric Categories
# --------------------------------------------------

st.subheader("Metric Categories")

category = pd.DataFrame({

"Category":[

"Traffic",

"Experiment",

"Segmentation",

"Quality",

"Statistics"

],

"Metrics":[

"Users, Sessions",

"Conversion, Lift",

"Region, Device",

"Duplicates, Freshness",

"P-value, Z-Test"

]

})

st.dataframe(
    category,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Formula Cards
# --------------------------------------------------

st.subheader("Important Formulae")

c1,c2=st.columns(2)

with c1:

    st.info("""

### Conversion Rate

Conversions ÷ Users ×100

""")

    st.info("""

### Relative Lift

(Treatment−Control)

÷

Control ×100

""")

    st.info("""

### Absolute Lift

Treatment−Control

""")

with c2:

    st.info("""

### Z Score

Difference

÷

Standard Error

""")

    st.info("""

### P-value

Probability that the

difference occurred

by chance.

""")

    st.info("""

### Confidence Interval

Difference ±1.96×SE

""")

# --------------------------------------------------
# Source Mapping
# --------------------------------------------------

st.subheader("Metric Source Mapping")

mapping=pd.DataFrame({

"Dashboard Page":[

"Executive Dashboard",

"A/B Analysis",

"Segmentation",

"Data Quality",

"Decision Center"

],

"Metrics Used":[

"Users, Conversion",

"Lift, P-value",

"Region, Device",

"Missing, Freshness",

"Winner"

],

"Data Source":[

"CSV",

"CSV",

"CSV",

"CSV",

"Calculated"

]

})

st.dataframe(
    mapping,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Data Dictionary
# --------------------------------------------------

st.subheader("Dataset Columns")

columns=pd.DataFrame({

"Column":df.columns,

"Data Type":[str(i) for i in df.dtypes]

})

st.dataframe(
    columns,
    use_container_width=True
)

# --------------------------------------------------
# KPI Usage
# --------------------------------------------------

st.subheader("Business Questions Answered")

questions=pd.DataFrame({

"Question":[

"Which Variant Wins?",

"Which Device Converts Best?",

"Which Region Performs Better?",

"Are Returning Users Better?",

"Is Data Healthy?",

"Can We Deploy?"

],

"Answered By":[

"Lift + P-value",

"Segmentation",

"Region Dashboard",

"Returning Analysis",

"Quality Dashboard",

"Decision Center"

]

})

st.dataframe(
    questions,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Download
# --------------------------------------------------

csv=dictionary.to_csv(index=False).encode("utf-8")

st.download_button(

"⬇ Download Metric Dictionary",

csv,

"metric_dictionary.csv",

"text/csv"

)