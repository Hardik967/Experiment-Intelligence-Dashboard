import pandas as pd
import streamlit as st

DATA_PATH = "data/ecommerce_conversion_ab_test_data.csv"


@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df = pd.read_csv(
    DATA_PATH,
    low_memory=False
)

    df.columns = df.columns.str.strip().str.lower()

    df.rename(
        columns={
            "tvc": "variant"
        },
        inplace=True
    )

    df["date"] = pd.to_datetime(df["date"])

    df["variant"] = df["variant"].astype(str)
    df["traffic_source"] = df["traffic_source"].astype(str)
    df["device_type"] = df["device_type"].astype(str)
    df["browser_language"] = df["browser_language"].astype(str)
    df["login_y_n"] = df["login_y_n"].astype(str)
    df["return_y_n"] = df["return_y_n"].astype(str)
    df["region"] = df["region"].astype(str)

    df["conversion"] = df["conversion"].astype(int)

    return df