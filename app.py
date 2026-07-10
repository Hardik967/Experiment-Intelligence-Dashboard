import streamlit as st

st.set_page_config(
    page_title="Experiment Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Experiment Intelligence Dashboard")

st.markdown("""
Welcome to the **Experiment Intelligence Dashboard**.

Use the sidebar to navigate through the analytics modules.

### Modules

- Executive Dashboard
- A/B Test Analysis
- Segmentation Analysis
- Data Quality
- Event Explorer
- Metric Dictionary
- Decision Center
""")

st.info(
    "This dashboard evaluates A/B experiments using statistical testing, "
    "conversion analytics, and decision-grade metrics."
)