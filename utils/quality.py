import pandas as pd


def missing_values(df):

    return (
        df
        .isnull()
        .sum()
        .reset_index()
        .rename(
            columns={
                "index": "Column",
                0: "Missing"
            }
        )
    )


def duplicate_rows(df):

    return df.duplicated().sum()


def freshness(df):

    latest = df["date"].max()

    return latest


def daily_records(df):

    return (
        df
        .groupby("date")
        .size()
        .reset_index(name="Records")
    )


def health_score(df):

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    score = 100

    score -= min(missing * 0.2, 20)

    score -= min(duplicates * 0.2, 20)

    return max(score, 0)


def invalid_conversions(df):

    return len(
        df[
            ~df["conversion"].isin([0, 1])
        ]
    )


def null_percentage(df):

    total = len(df)

    percent = (
        df
        .isnull()
        .sum()
        / total
        * 100
    )

    return percent.reset_index().rename(
        columns={
            "index": "Column",
            0: "Null %"
        }
    )