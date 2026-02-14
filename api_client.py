"""
Football API Client for Serie A Data

This module fetches live standings and fixtures from the API-Football service.
Configure your API key via:
1. Streamlit secrets (st.secrets["FOOTBALL_API_KEY"])
2. Environment variable (FOOTBALL_API_KEY)
3. .env file (FOOTBALL_API_KEY=xxx)
"""

import os
import requests
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip, timedelta


# ==========================================
# CONFIGURATION
# ==========================================

API_BASE_URL = "https://v3.football.api-sports.io"
SERIE_A_LEAGUE_ID = 135  # Serie A league ID in API-Football
CURRENT_SEASON = 2025    # 2025/26 season


def get_api_key() -> str:
    """
    Get API key from Streamlit secrets, environment variable, or .env file.

    Returns:
        API key string

    Raises:
        ValueError: If API key is not configured
    """
    # Try Streamlit secrets first (for deployed apps)
    try:
        import streamlit as st
        if "FOOTBALL_API_KEY" in st.secrets:
            return st.secrets["FOOTBALL_API_KEY"]
    except Exception:
        pass  # Not running in Streamlit or secrets not configured

    # Fall back to environment variable
    api_key = os.environ.get("FOOTBALL_API_KEY")
    if api_key and api_key != "your-api-key-here":
        return api_key

    raise ValueError(
        "FOOTBALL_API_KEY not configured. "
        "Set it in Streamlit secrets, environment variable, or .env file."
    )


def _make_request(endpoint: str, params: Dict = None) -> Dict:
    """
    Make authenticated request to API-Football.

    Args:
        endpoint: API endpoint (e.g., "/standings")
        params: Query parameters

    Returns:
        JSON response as dictionary

    Raises:
        requests.RequestException: On network errors
        ValueError: On API errors
    """
    headers = {
        "x-apisports-key": get_api_key(),
        "x-apisports-host": "v3.football.api-sports.io"
    }

    url = f"{API_BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers, params=params or {})
    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise ValueError(f"API Error: {data['errors']}")

    return data


# ==========================================
# STANDINGS DATA
# ==========================================

def fetch_standings() -> Dict[str, Dict[str, int]]:
    """
    Fetch current Serie A standings.

    Returns:
        Dictionary mapping team names to their stats:
        {
            'TeamName': {'Pts': int, 'GF': int, 'GA': int},
            ...
        }
    """
    data = _make_request("/standings", {
        "league": SERIE_A_LEAGUE_ID,
        "season": CURRENT_SEASON
    })

    standings = data["response"][0]["league"]["standings"][0]

    teams_data = {}
    for team_entry in standings:
        team_name = team_entry["team"]["name"]
        teams_data[team_name] = {
            "Pts": team_entry["points"],
            "GF": team_entry["all"]["goals"]["for"],
            "GA": team_entry["all"]["goals"]["against"],
        }

    return teams_data


def fetch_standings_with_form() -> Tuple[Dict[str, Dict[str, int]], Dict[str, List[int]]]:
    """
    Fetch current Serie A standings including recent form.

    Returns:
        Tuple of:
        - teams_data: {'TeamName': {'Pts': int, 'GF': int, 'GA': int}, ...}
        - form_data: {'TeamName': [3, 0, 1, 3, 3], ...} (points from last 5 games)
    """
    data = _make_request("/standings", {
        "league": SERIE_A_LEAGUE_ID,
        "season": CURRENT_SEASON
    })

    standings = data["response"][0]["league"]["standings"][0]

    teams_data = {}
    form_data = {}

    for team_entry in standings:
        team_name = team_entry["team"]["name"]

        # Basic stats
        teams_data[team_name] = {
            "Pts": team_entry["points"],
            "GF": team_entry["all"]["goals"]["for"],
            "GA": team_entry["all"]["goals"]["against"],
        }

        # Form string (e.g., "WDLWW")
        form_string = team_entry.get("form", "")
        if form_string:
            # Convert form string to points list
            # W = 3, D = 1, L = 0
            form_points = []
            for char in form_string[-5:]:  # Last 5 results
                if char == "W":
                    form_points.append(3)
                elif char == "D":
                    form_points.append(1)
                else:  # "L"
                    form_points.append(0)
            form_data[team_name] = form_points

    return teams_data, form_data


# ==========================================
# FIXTURES DATA
# ==========================================

def fetch_remaining_fixtures() -> List[Tuple[str, str]]:
    """
    Fetch remaining Serie A fixtures for the current season.

    Returns:
        List of tuples (home_team, away_team) for matches not yet played.
    """
    # Get fixtures that are scheduled or not started
    data = _make_request("/fixtures", {
        "league": SERIE_A_LEAGUE_ID,
        "season": CURRENT_SEASON,
        "status": "NS-TBD-PST"  # Not Started, To Be Defined, Postponed
    })

    fixtures = []
    for match in data["response"]:
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]
        fixtures.append((home_team, away_team))

    return fixtures


def fetch_fixtures_by_date_range(
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> List[Tuple[str, str]]:
    """
    Fetch Serie A fixtures within a date range.

    Args:
        from_date: Start date in YYYY-MM-DD format (defaults to today)
        to_date: End date in YYYY-MM-DD format (defaults to end of season)

    Returns:
        List of tuples (home_team, away_team).
    """
    if from_date is None:
        from_date = datetime.now().strftime("%Y-%m-%d")

    if to_date is None:
        # End of season (approximate)
        to_date = f"{CURRENT_SEASON + 1}-05-31"

    data = _make_request("/fixtures", {
        "league": SERIE_A_LEAGUE_ID,
        "season": CURRENT_SEASON,
        "from": from_date,
        "to": to_date,
    })

    fixtures = []
    for match in data["response"]:
        # Only include matches that haven't been played
        status = match["fixture"]["status"]["short"]
        if status in ["NS", "TBD", "PST"]:  # Not Started, TBD, Postponed
            home_team = match["teams"]["home"]["name"]
            away_team = match["teams"]["away"]["name"]
            fixtures.append((home_team, away_team))

    return fixtures


# ==========================================
# MATCHDAY INFORMATION
# ==========================================

def get_current_matchday() -> int:
    """
    Get the current matchday number.

    Returns:
        Current matchday (round) number.
    """
    data = _make_request("/fixtures/rounds", {
        "league": SERIE_A_LEAGUE_ID,
        "season": CURRENT_SEASON,
        "current": "true"
    })

    if data["response"]:
        # Format is typically "Regular Season - X"
        round_str = data["response"][0]
        try:
            return int(round_str.split("-")[-1].strip())
        except (ValueError, IndexError):
            return 1
    return 1


# ==========================================
# DATA LOADING FUNCTIONS
# ==========================================

def load_live_data() -> Tuple[Dict[str, Dict[str, int]], Dict[str, List[int]], List[Tuple[str, str]]]:
    """
    Load all required data from the API.

    Returns:
        Tuple of:
        - teams_data: Current standings with points and goals
        - form_data: Recent form (last 5 matches) as points
        - fixtures: Remaining fixtures as (home, away) tuples
    """
    teams_data, form_data = fetch_standings_with_form()
    fixtures = fetch_remaining_fixtures()

    return teams_data, form_data, fixtures


# ==========================================
# TEAM NAME MAPPING
# ==========================================

# API team names may differ from local names - add mappings here if needed
TEAM_NAME_MAPPING = {
    # "API Name": "Local Name",
    # Add mappings as needed
}


def normalize_team_name(api_name: str) -> str:
    """
    Normalize team name from API to local naming convention.

    Args:
        api_name: Team name as returned by API

    Returns:
        Normalized team name
    """
    return TEAM_NAME_MAPPING.get(api_name, api_name)


def apply_name_mapping(
    teams_data: Dict[str, Dict[str, int]],
    form_data: Dict[str, List[int]],
    fixtures: List[Tuple[str, str]]
) -> Tuple[Dict[str, Dict[str, int]], Dict[str, List[int]], List[Tuple[str, str]]]:
    """
    Apply team name mapping to all data structures.

    Args:
        teams_data: Standings data
        form_data: Form data
        fixtures: Fixtures list

    Returns:
        Tuple with normalized data
    """
    normalized_teams = {
        normalize_team_name(k): v for k, v in teams_data.items()
    }

    normalized_form = {
        normalize_team_name(k): v for k, v in form_data.items()
    }

    normalized_fixtures = [
        (normalize_team_name(home), normalize_team_name(away))
        for home, away in fixtures
    ]

    return normalized_teams, normalized_form, normalized_fixtures


# ==========================================
# TESTING / CLI
# ==========================================

if __name__ == "__main__":
    """Test the API client by fetching current data."""

    print("Fetching Serie A data from API-Football...")
    print("-" * 50)

    try:
        teams, form, fixtures = load_live_data()

        print(f"\n📊 Standings ({len(teams)} teams):")
        for team, stats in sorted(teams.items(), key=lambda x: x[1]['Pts'], reverse=True):
            form_str = "".join(["W" if p == 3 else "D" if p == 1 else "L" for p in form.get(team, [])])
            print(f"  {team:20} - Pts: {stats['Pts']:2}, GF: {stats['GF']:2}, GA: {stats['GA']:2}, Form: {form_str}")

        print(f"\n📅 Remaining Fixtures ({len(fixtures)} matches):")
        for i, (home, away) in enumerate(fixtures[:10], 1):
            print(f"  {i}. {home} vs {away}")
        if len(fixtures) > 10:
            print(f"  ... and {len(fixtures) - 10} more matches")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except requests.RequestException as e:
        print(f"❌ Network Error: {e}")

