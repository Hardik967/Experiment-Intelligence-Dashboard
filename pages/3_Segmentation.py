import streamlit as st
import plotly.express as px
import pandas as pd

from utils.loader import load_data

st.set_page_config(
    page_title="Segmentation Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Segmentation Analysis")

st.markdown(
    "Analyze experiment performance across different user segments."
)

df = load_data()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("Filters")

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

source = st.sidebar.multiselect(
    "Traffic Source",
    sorted(df["traffic_source"].unique()),
    default=sorted(df["traffic_source"].unique())
)

filtered = df[
    df["variant"].isin(variant)
    &
    df["device_type"].isin(device)
    &
    df["traffic_source"].isin(source)
]

st.success(f"Records : {len(filtered):,}")

# -------------------------------------------------
# Device Performance
# -------------------------------------------------

device_df = (
    filtered
    .groupby("device_type")
    .agg(
        Users=("conversion","count"),
        Conversion=("conversion","mean")
    )
    .reset_index()
)

device_df["Conversion"] *= 100

left,right = st.columns(2)

with left:

    fig = px.bar(
        device_df,
        x="device_type",
        y="Users",
        color="device_type",
        title="Users by Device"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.bar(
        device_df,
        x="device_type",
        y="Conversion",
        color="device_type",
        title="Conversion Rate by Device"
    )

    st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Traffic Source
# -------------------------------------------------

traffic = (
    filtered
    .groupby("traffic_source")
    .agg(
        Users=("conversion","count"),
        Conversion=("conversion","mean")
    )
    .reset_index()
)

traffic["Conversion"]*=100

fig=px.bar(
    traffic,
    x="traffic_source",
    y="Conversion",
    color="traffic_source",
    title="Traffic Source Performance"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Region Analysis
# -------------------------------------------------

region=(
    filtered
    .groupby("region")
    .agg(
        Users=("conversion","count"),
        Conversion=("conversion","mean")
    )
    .reset_index()
)

region["Conversion"]*=100

fig=px.bar(
    region,
    x="region",
    y="Conversion",
    color="region",
    title="Region Conversion Rate"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Browser Language
# -------------------------------------------------

language=(
    filtered
    .groupby("browser_language")
    .agg(
        Users=("conversion","count"),
        Conversion=("conversion","mean")
    )
    .reset_index()
)

language["Conversion"]*=100

fig=px.bar(
    language,
    x="browser_language",
    y="Conversion",
    color="browser_language",
    title="Browser Language Performance"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Login Status
# -------------------------------------------------

login=(
    filtered
    .groupby("login_y_n")
    .agg(
        Users=("conversion","count"),
        Conversion=("conversion","mean")
    )
    .reset_index()
)

login["Conversion"]*=100

left,right=st.columns(2)

with left:

    fig=px.pie(
        login,
        names="login_y_n",
        values="Users",
        title="Logged vs Guest Users"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig=px.bar(
        login,
        x="login_y_n",
        y="Conversion",
        color="login_y_n",
        title="Login Conversion Rate"
    )

    st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Returning Users
# -------------------------------------------------

ret=(
    filtered
    .groupby("return_y_n")
    .agg(
        Users=("conversion","count"),
        Conversion=("conversion","mean")
    )
    .reset_index()
)

ret["Conversion"]*=100

left,right=st.columns(2)

with left:

    fig=px.pie(
        ret,
        names="return_y_n",
        values="Users",
        title="Returning vs New Users"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig=px.bar(
        ret,
        x="return_y_n",
        y="Conversion",
        color="return_y_n",
        title="Returning User Conversion"
    )

    st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Variant Heatmap
# -------------------------------------------------

heat=(
    filtered
    .groupby(
        ["device_type","variant"]
    )
    .agg(
        Conversion=("conversion","mean")
    )
    .reset_index()
)

heat["Conversion"]*=100

pivot=heat.pivot(
    index="device_type",
    columns="variant",
    values="Conversion"
)

fig=px.imshow(
    pivot,
    text_auto=".2f",
    title="Variant Performance by Device"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------
# Segment Summary
# -------------------------------------------------

summary=(
    filtered
    .groupby(
        [
            "variant",
            "device_type",
            "traffic_source"
        ]
    )
    .agg(
        Users=("conversion","count"),
        Conversions=("conversion","sum"),
        Conversion_Rate=("conversion","mean")
    )
    .reset_index()
)

summary["Conversion_Rate"]*=100

st.subheader("Segment Summary")

st.dataframe(
    summary,
    use_container_width=True,
    height=450
)

# -------------------------------------------------
# Best Performing Segment
# -------------------------------------------------

best=summary.sort_values(
    "Conversion_Rate",
    ascending=False
).head(1)

st.success(
    f"""
### Best Performing Segment

Variant : **{best.iloc[0]['variant']}**

Device : **{best.iloc[0]['device_type']}**

Traffic Source : **{best.iloc[0]['traffic_source']}**

Conversion Rate : **{best.iloc[0]['Conversion_Rate']:.2f}%**
"""
)

# -------------------------------------------------
# Download
# -------------------------------------------------

csv=summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Segment Summary",
    csv,
    "segment_summary.csv",
    "text/csv"
)