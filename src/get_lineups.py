from nba_api.stats.endpoints import leaguedashlineups
from nba_api.stats.static import teams
import pandas as pd
import time 
from pathlib import Path 

def get_heat_team_id() -> int: 

    """Return the team_id for the Miami Heat."""

    nba_teams = teams.get_teams()
    heat = [t for t in nba_teams if t["full_name"] == "Miami Heat"]
    if not heat: 
        raise ValueError("Miami Heat team not found.")
    return heat[0]["id"]  # type: ignore[index]

def fetch_heat_lineups(season: str = "2025-26", 
                       season_type: str = "Regular Season", 
                       group_quantity: int = 5) -> pd.DataFrame:
    
    """
    Fetch Miami Heat lineups from the NBA API and return as a DataFrame.
    """

    team_id = get_heat_team_id() 
    print(f"Using team_id={team_id} for Miami Heat.")

    lineups = leaguedashlineups.LeagueDashLineups(
        season=season,
        season_type_all_star=season_type,
        per_mode_detailed="PerGame", 
        measure_type_detailed_defense="Advanced",
        group_quantity=group_quantity,
        team_id_nullable=team_id
    )

    df = lineups.get_data_frames()[0]
    print(f"Fetched {len(df)} lineup rows.") 
    return df 

def save_raw_lineups(df: pd.DataFrame, 
                     season: str = "2025-26",
                     season_type: str = "Regular Season", 
                     group_quantity: int = 5) -> Path: 
    
    """
    Save the raw lineup DataFrame to data/raw and return the path.
    """
    # make sure data/raw exists
    raw_dir = Path("data") / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    safe_season_type = season_type.replace(" ", "_")
    filename = f"heat_lineups_{group_quantity}man_{season}_{safe_season_type}.csv"
    filepath = raw_dir / filename

    df.to_csv(filepath, index=False)
    print(f"Saved raw lineup data to: {filepath.resolve()}")
    return filepath

if __name__ == "__main__": 
    SEASON = "2025-26"
    SEASON_TYPE = "Regular Season"
    GROUP_QUANTITY = 5

    df_lineups = fetch_heat_lineups(
        season=SEASON,
        season_type=SEASON_TYPE,
        group_quantity=GROUP_QUANTITY
    )

save_raw_lineups(df_lineups, SEASON, SEASON_TYPE, GROUP_QUANTITY)