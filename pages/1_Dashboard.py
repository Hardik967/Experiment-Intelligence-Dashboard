import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.loader import load_data
from utils.database import create_database
from utils.metrics import *

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📈",
    layout="wide"
)

df = load_data()

# Create SQLite database on first load
create_database(df)

st.title("📈 Executive Dashboard")

st.markdown("Monitor experiment performance using real conversion data.")

# ----------------------------
# Sidebar Filters
# ----------------------------

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
    (df["variant"].isin(variant))
    &
    (df["device_type"].isin(device))
    &
    (df["traffic_source"].isin(source))
    &
    (df["region"].isin(region))
    &
    (df["login_y_n"].isin(login))
    &
    (df["return_y_n"].isin(returning))
]

st.success(f"Filtered Records : {len(filtered):,}")

# ----------------------------
# KPI Cards
# ----------------------------

users = total_users(filtered)
conversions = total_conversions(filtered)
rate = conversion_rate(filtered)

variant_df = variant_summary(filtered)

if len(variant_df) >= 2:
    lift = (
        (
            variant_df.iloc[1]["Conversion Rate"]
            -
            variant_df.iloc[0]["Conversion Rate"]
        )
        /
        variant_df.iloc[0]["Conversion Rate"]
    ) * 100
else:
    lift = 0

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Total Users",
    f"{users:,}"
)

c2.metric(
    "✅ Conversions",
    f"{conversions:,}"
)

c3.metric(
    "📊 Conversion Rate",
    f"{rate:.2f}%"
)

c4.metric(
    "🚀 Relative Lift",
    f"{lift:.2f}%"
)

st.divider()

# ----------------------------
# Variant Performance
# ----------------------------

left, right = st.columns(2)

with left:

    fig = px.bar(
        variant_df,
        x="variant",
        y="Conversion Rate",
        text="Conversion Rate",
        title="Conversion Rate by Variant"
    )

    fig.update_traces(texttemplate="%{text:.2f}")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.pie(
        variant_df,
        values="Users",
        names="variant",
        title="Traffic Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# Daily Trend
# ----------------------------

daily = (
    filtered
    .groupby("date")
    .agg(
        Users=("conversion", "count"),
        Conversion=("conversion", "mean")
    )
    .reset_index()
)

daily["Conversion"] *= 100

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["Users"],
        mode="lines",
        name="Users"
    )
)

fig.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["Conversion"],
        mode="lines",
        yaxis="y2",
        name="Conversion %"
    )
)

fig.update_layout(

    title="Daily Activity",

    yaxis=dict(title="Users"),

    yaxis2=dict(
        title="Conversion %",
        overlaying="y",
        side="right"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# Device Analysis
# ----------------------------

device_df = device_summary(filtered)

device_df["Conversion_Rate"] *= 100

left, right = st.columns(2)

with left:

    fig = px.bar(
        device_df,
        x="device_type",
        y="Users",
        title="Users by Device"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.bar(
        device_df,
        x="device_type",
        y="Conversion_Rate",
        title="Device Conversion Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# Traffic Source
# ----------------------------

traffic = traffic_summary(filtered)

traffic["Conversion_Rate"] *= 100

fig = px.bar(
    traffic,
    x="traffic_source",
    y="Conversion_Rate",
    color="traffic_source",
    title="Traffic Source Conversion"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# Region
# ----------------------------

region_df = region_summary(filtered)

region_df["Conversion_Rate"] *= 100

fig = px.bar(
    region_df,
    x="region",
    y="Conversion_Rate",
    color="region",
    title="Region Performance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# Login Analysis
# ----------------------------

login_df = login_summary(filtered)

login_df["Conversion_Rate"] *= 100

left, right = st.columns(2)

with left:

    fig = px.bar(
        login_df,
        x="login_y_n",
        y="Users",
        title="Logged-in Users"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.bar(
        login_df,
        x="login_y_n",
        y="Conversion_Rate",
        title="Login Conversion Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# Returning Users
# ----------------------------

ret = return_summary(filtered)

ret["Conversion_Rate"] *= 100

fig = px.bar(
    ret,
    x="return_y_n",
    y="Conversion_Rate",
    color="return_y_n",
    title="Returning Users Conversion"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# Variant Summary Table
# ----------------------------

st.subheader("Variant Summary")

display = variant_df.copy()

display["Conversion Rate"] = (
    display["Conversion Rate"]
    .round(2)
)

st.dataframe(
    display,
    use_container_width=True,
    height=250
)

# ----------------------------
# Download
# ----------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_experiment_data.csv",
    "text/csv"
)