"""
Thin wrapper around nba_api with rate limiting
"""
import time
from datetime import date

import pandas as pd
from nba_api.stats.endpoints import leaguegamelog, shotchartdetail

PAUSE_SECONDS = 1.5
TIMEOUT_SECONDS = 60
SEASON_TYPE = "Regular Season"

def season_for(day: date) -> str:
    """
    NBA season label for a date, e.g. 2026-01-15 -> '2025-26'
    Season start in October, so Oct-Dec belong to the season
    starting that year.
    """
    start_year = day.year if day.month >= 10 else day.year - 1
    return f"{start_year}-{str(start_year +1)[2:]}"

def _fmt(day: date) -> str:
    return day.strftime("%m/%d/%Y") # NBA API format

def fetch_game_logs(season: str, level: str, date_from: date, date_to: date) -> pd.DataFrame:
    """
    level = 'T' for team rows, 'P' for player rows.
    """
    response = leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star=SEASON_TYPE,
        player_or_team_abbreviation=level,
        date_from_nullable=_fmt(date_from),
        date_to_nullable=_fmt(date_to),
        timeout=TIMEOUT_SECONDS
    )
    time.sleep(PAUSE_SECONDS)
    return response.get_data_frames()[0]

def fetch_shots(season: str, date_from: date, date_to: date) -> pd.DataFrame:
    """
    Every field goal attempt (made and missed) in the date range.
    """
    response = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=0,
        season_nullable=season,
        season_type_all_star=SEASON_TYPE,
        context_measure_simple="FGA",
        date_from_nullable=_fmt(date_from),
        date_to_nullable=_fmt(date_to),
        timeout=TIMEOUT_SECONDS
    )
    time.sleep(PAUSE_SECONDS)
    return response.get_data_frames()[0]
