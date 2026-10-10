"""
Load DataFrames into the raw schema; safe to re-run
"""
from datetime import date

import pandas as pd
from sqlalchemy import inspect, text

from ingestion.db import get_engine

def load_raw(df: pd.DataFrame, table: str, date_col: str, date_format: str,
             date_from: date, date_to: date) -> int:
    """ Replace one date range of raw.<table> with the rows in df. """
    if df.empty:
        return 0 

    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    df['game_day'] = pd.to_datetime(
        df[date_col.lower()],
        format=date_format
    ).dt.date
    df['loaded_at'] = pd.Timestamp.now(tz="UTC")

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("create schema if not exists raw"))
        if inspect(conn).has_table(table, schema="raw"):
            conn.execute(
                text(f"delete from raw.{table} where game_day between :start and :end", {"start": date_from, "end": date_to})
            )
        df.to_sql(table, conn, schema="raw", if_exists="append", index=False)
    return len(df)
