import sqlite3
import pandas as pd

DB_PATH = "database/experiments.db"


def create_database(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "experiments",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()

    conn.close()


def run_query(query):

    conn = sqlite3.connect(DB_PATH)

    result = pd.read_sql(query, conn)

    conn.close()

    return result