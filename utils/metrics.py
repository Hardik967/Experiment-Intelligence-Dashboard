import pandas as pd


def total_users(df):

    return len(df)


def total_conversions(df):

    return df["conversion"].sum()


def conversion_rate(df):

    return (
        df["conversion"].mean() * 100
    )


def variant_summary(df):

    summary = (
        df
        .groupby("variant")
        .agg(
            Users=("conversion", "count"),
            Conversions=("conversion", "sum")
        )
        .reset_index()
    )

    summary["Conversion Rate"] = (
        summary["Conversions"]
        /
        summary["Users"]
        * 100
    )

    return summary


def traffic_summary(df):

    return (
        df
        .groupby("traffic_source")
        .agg(
            Users=("conversion", "count"),
            Conversion_Rate=("conversion", "mean")
        )
        .reset_index()
    )


def device_summary(df):

    return (
        df
        .groupby("device_type")
        .agg(
            Users=("conversion", "count"),
            Conversion_Rate=("conversion", "mean")
        )
        .reset_index()
    )


def region_summary(df):

    return (
        df
        .groupby("region")
        .agg(
            Users=("conversion", "count"),
            Conversion_Rate=("conversion", "mean")
        )
        .reset_index()
    )


def login_summary(df):

    return (
        df
        .groupby("login_y_n")
        .agg(
            Users=("conversion", "count"),
            Conversion_Rate=("conversion", "mean")
        )
        .reset_index()
    )


def return_summary(df):

    return (
        df
        .groupby("return_y_n")
        .agg(
            Users=("conversion", "count"),
            Conversion_Rate=("conversion", "mean")
        )
        .reset_index()
    )