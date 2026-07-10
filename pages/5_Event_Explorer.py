import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_data
from utils.database import run_query

st.set_page_config(
    page_title="Event Explorer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Event Explorer")

st.markdown(
    "Explore raw experiment events using interactive filters."
)

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Event Filters")

variant = st.sidebar.multiselect(
    "Variant",
    sorted(df["variant"].unique()),
    default=sorted(df["variant"].unique())
)

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

language = st.sidebar.multiselect(
    "Browser Language",
    sorted(df["browser_language"].unique()),
    default=sorted(df["browser_language"].unique())
)

login = st.sidebar.multiselect(
    "Login Status",
    sorted(df["login_y_n"].unique()),
    default=sorted(df["login_y_n"].unique())
)

returning = st.sidebar.multiselect(
    "Returning User",
    sorted(df["return_y_n"].unique()),
    default=sorted(df["return_y_n"].unique())
)

date_range = st.sidebar.date_input(
    "Date Range",
    [
        df["date"].min(),
        df["date"].max()
    ]
)

filtered = df[
    (df["variant"].isin(variant))
    &
    (df["device_type"].isin(device))
    &
    (df["traffic_source"].isin(traffic))
    &
    (df["region"].isin(region))
    &
    (df["browser_language"].isin(language))
    &
    (df["login_y_n"].isin(login))
    &
    (df["return_y_n"].isin(returning))
    &
    (
        df["date"].dt.date.between(
            date_range[0],
            date_range[1]
        )
    )
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Events", f"{len(filtered):,}")

c2.metric(
    "Conversions",
    int(filtered["conversion"].sum())
)

c3.metric(
    "Conversion %",
    f"{filtered['conversion'].mean()*100:.2f}%"
)

c4.metric(
    "Unique Regions",
    filtered["region"].nunique()
)

st.divider()

# --------------------------------------------------
# Search
# --------------------------------------------------

keyword = st.text_input(
    "Search Region / Source / Device"
)

if keyword:

    keyword = keyword.lower()

    filtered = filtered[
        filtered.astype(str)
        .apply(
            lambda row:
            row.str.lower()
            .str.contains(keyword)
            .any(),
            axis=1
        )
    ]

# --------------------------------------------------
# Event Table
# --------------------------------------------------

st.subheader("Experiment Events")

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

# --------------------------------------------------
# SQL Explorer
# --------------------------------------------------

st.subheader("SQL Insights")

query_option = st.selectbox(
    "Choose Query",
    [
        "Variant Summary",
        "Traffic Summary",
        "Region Summary",
        "Device Summary"
    ]
)

if query_option == "Variant Summary":

    sql = """
    SELECT
        variant,
        COUNT(*) AS Users,
        SUM(conversion) AS Conversions,
        ROUND(
            AVG(conversion)*100,
            2
        ) AS Conversion_Rate
    FROM experiments
    GROUP BY variant
    """

elif query_option == "Traffic Summary":

    sql = """
    SELECT
        traffic_source,
        COUNT(*) Users,
        ROUND(
            AVG(conversion)*100,
            2
        ) Conversion_Rate
    FROM experiments
    GROUP BY traffic_source
    """

elif query_option == "Region Summary":

    sql = """
    SELECT
        region,
        COUNT(*) Users,
        ROUND(
            AVG(conversion)*100,
            2
        ) Conversion_Rate
    FROM experiments
    GROUP BY region
    """

else:

    sql = """
    SELECT
        device_type,
        COUNT(*) Users,
        ROUND(
            AVG(conversion)*100,
            2
        ) Conversion_Rate
    FROM experiments
    GROUP BY device_type
    """

result = run_query(sql)

st.code(sql, language="sql")

st.dataframe(
    result,
    use_container_width=True
)

# --------------------------------------------------
# Daily Events
# --------------------------------------------------

daily = (
    filtered
    .groupby("date")
    .size()
    .reset_index(name="Events")
)

fig = px.line(
    daily,
    x="date",
    y="Events",
    markers=True,
    title="Daily Event Volume"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Region Distribution
# --------------------------------------------------

region_df = (
    filtered["region"]
    .value_counts()
    .reset_index()
)

region_df.columns = [
    "Region",
    "Users"
]

fig = px.bar(
    region_df,
    x="Region",
    y="Users",
    color="Region",
    title="Region Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Device Distribution
# --------------------------------------------------

device_df = (
    filtered["device_type"]
    .value_counts()
    .reset_index()
)

device_df.columns = [
    "Device",
    "Users"
]

fig = px.pie(
    device_df,
    names="Device",
    values="Users",
    title="Device Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Conversion Distribution
# --------------------------------------------------

conversion_df = (
    filtered["conversion"]
    .value_counts()
    .reset_index()
)

conversion_df.columns = [
    "Conversion",
    "Count"
]

fig = px.bar(
    conversion_df,
    x="Conversion",
    y="Count",
    color="Conversion",
    title="Conversion Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Dataset Statistics
# --------------------------------------------------

st.subheader("Dataset Statistics")

stats = pd.DataFrame({
    "Metric":[
        "Rows",
        "Columns",
        "Variants",
        "Regions",
        "Devices",
        "Traffic Sources"
    ],
    "Value":[
        len(filtered),
        len(filtered.columns),
        filtered["variant"].nunique(),
        filtered["region"].nunique(),
        filtered["device_type"].nunique(),
        filtered["traffic_source"].nunique()
    ]
})

st.dataframe(
    stats,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Downloads
# --------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "experiment_events.csv",
    "text/csv"
)

import os

os.makedirs("exports", exist_ok=True)

if len(filtered) > 1048576:

    st.warning(
        "Dataset exceeds Excel's maximum row limit.\n\n"
        "CSV download contains all records.\n"
        "Excel download is limited to 1,048,576 rows."
    )

excel_df = filtered.head(1048576)

excel_path = "exports/event_explorer.xlsx"

excel_df.to_excel(
    excel_path,
    index=False
)

with open(excel_path, "rb") as f:

    st.download_button(
        "⬇ Download Excel",
        data=f,
        file_name="event_explorer.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )