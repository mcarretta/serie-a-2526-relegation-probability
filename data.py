"""
Serie A 2025/26 Season Data

This module contains all the team data, fixtures, and form information
for the Serie A 2025/26 season simulation.

Data can be loaded from:
1. Live API (API-Football) when FOOTBALL_API_KEY is set
2. Static fallback data defined in this module
"""

import os
import logging
from typing import Dict, List, Tuple, Optional

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip

# ==========================================
# DATA SOURCE CONFIGURATION
# ==========================================

# Set to True to force using static data even if API key is available
USE_STATIC_DATA = False

# Module-level data holders (populated on first access)
_teams_data: Optional[Dict[str, Dict[str, int]]] = None
_last_5_performance: Optional[Dict[str, List[int]]] = None
_fixtures: Optional[List[Tuple[str, str]]] = None
_data_source: str = "not loaded"

logger = logging.getLogger(__name__)

# ==========================================
# TEAM DATA
# ==========================================

# Points, Goals For (GF), Goals Against (GA) after 24 matchdays
TEAMS_DATA: Dict[str, Dict[str, int]] = {
    # --- Relegation Battle teams ---
    'Lazio': {'Pts': 33, 'GF': 26, 'GA': 23},
    'Udinese': {'Pts': 32, 'GF': 27, 'GA': 36},
    'Bologna': {'Pts': 30, 'GF': 32, 'GA': 31},
    'Sassuolo': {'Pts': 29, 'GF': 27, 'GA': 34},
    'Cagliari': {'Pts': 28, 'GF': 28, 'GA': 33},
    'Torino': {'Pts': 27, 'GF': 24, 'GA': 42},
    'Parma': {'Pts': 26, 'GF': 16, 'GA': 30},
    'Genoa': {'Pts': 23, 'GF': 29, 'GA': 37},
    'Cremonese': {'Pts': 23, 'GF': 21, 'GA': 33},
    'Lecce': {'Pts': 21, 'GF': 15, 'GA': 31},
    'Fiorentina': {'Pts': 18, 'GF': 27, 'GA': 38},
    'Pisa': {'Pts': 15, 'GF': 19, 'GA': 40},
    'Verona': {'Pts': 15, 'GF': 18, 'GA': 41},
    # --- Top/Mid Table teams ---
    'Inter': {'Pts': 58, 'GF': 57, 'GA': 19},
    'Milan': {'Pts': 50, 'GF': 38, 'GA': 17},
    'Napoli': {'Pts': 49, 'GF': 36, 'GA': 23},
    'Juventus': {'Pts': 46, 'GF': 41, 'GA': 20},
    'Roma': {'Pts': 46, 'GF': 29, 'GA': 14},
    'Como': {'Pts': 41, 'GF': 37, 'GA': 16},
    'Atalanta': {'Pts': 39, 'GF': 32, 'GA': 21},
}


# ==========================================
# RECENT FORM
# ==========================================

# Points earned in last 5 games (3=Win, 1=Draw, 0=Loss)
LAST_5_PERFORMANCE: Dict[str, List[int]] = {
    'Inter': [3, 3, 3, 3, 3],
    'Napoli': [1, 3, 0, 3, 3],
    'Milan': [1, 3, 3, 1, 3],
    'Juventus': [3, 0, 3, 3, 1],
    'Atalanta': [3, 1, 3, 1, 3],
    'Roma': [3, 3, 1, 0, 3],
    'Como': [1, 0, 3, 3, 1],
    'Lazio': [3, 0, 1, 3, 1],
    'Udinese': [1, 0, 3, 3, 0],
    'Bologna': [3, 0, 0, 0, 0],
    'Sassuolo': [0, 0, 3, 3, 0],
    'Cagliari': [0, 3, 3, 3, 0],
    'Torino': [0, 0, 0, 3, 1],
    'Parma': [1, 1, 0, 0, 3],
    'Genoa': [3, 1, 3, 0, 0],
    'Cremonese': [0, 1, 0, 0, 0],
    'Lecce': [0, 0, 1, 0, 3],
    'Fiorentina': [1, 3, 0, 0, 1],
    'Pisa': [1, 1, 0, 0, 1],
    'Verona': [0, 1, 0, 0, 1],
}


# ==========================================
# REMAINING FIXTURES
# ==========================================

# Remaining fixtures from Matchday 25 to 38
FIXTURES: List[Tuple[str, str]] = [
    # Matchday 25
    ('Pisa', 'Milan'), ('Como', 'Fiorentina'), ('Lazio', 'Atalanta'), ('Inter', 'Juventus'),
    ('Udinese', 'Sassuolo'), ('Parma', 'Verona'), ('Cremonese', 'Genoa'), ('Torino', 'Bologna'),
    ('Napoli', 'Roma'), ('Cagliari', 'Lecce'),

    # Matchday 24 (Rescheduled)
    ('Milan', 'Como'),

    # Matchday 26
    ('Sassuolo', 'Verona'), ('Juventus', 'Como'), ('Lecce', 'Inter'), ('Cagliari', 'Lazio'),
    ('Genoa', 'Torino'), ('Atalanta', 'Napoli'), ('Milan', 'Parma'), ('Roma', 'Cremonese'),
    ('Fiorentina', 'Pisa'), ('Bologna', 'Udinese'),

    # Matchday 27
    ('Inter', 'Genoa'), ('Udinese', 'Fiorentina'), ('Cremonese', 'Milan'), ('Verona', 'Napoli'),
    ('Parma', 'Cagliari'), ('Pisa', 'Bologna'), ('Torino', 'Lazio'), ('Roma', 'Juventus'),
    ('Sassuolo', 'Atalanta'), ('Como', 'Lecce'),

    # Matchday 28
    ('Cagliari', 'Como'), ('Juventus', 'Pisa'), ('Bologna', 'Verona'), ('Lecce', 'Cremonese'),
    ('Genoa', 'Roma'), ('Atalanta', 'Udinese'), ('Napoli', 'Torino'), ('Lazio', 'Sassuolo'),
    ('Milan', 'Inter'), ('Fiorentina', 'Parma'),

    # Matchday 29
    ('Pisa', 'Cagliari'), ('Verona', 'Genoa'), ('Lazio', 'Milan'), ('Cremonese', 'Fiorentina'),
    ('Sassuolo', 'Bologna'), ('Torino', 'Parma'), ('Inter', 'Atalanta'), ('Napoli', 'Lecce'),
    ('Como', 'Roma'), ('Udinese', 'Juventus'),

    # Matchday 30
    ('Juventus', 'Sassuolo'), ('Parma', 'Cremonese'), ('Cagliari', 'Napoli'), ('Atalanta', 'Verona'),
    ('Roma', 'Lecce'), ('Genoa', 'Udinese'), ('Bologna', 'Lazio'), ('Fiorentina', 'Inter'),
    ('Milan', 'Torino'), ('Como', 'Pisa'),

    # Matchday 31
    ('Lazio', 'Parma'), ('Napoli', 'Milan'), ('Cremonese', 'Bologna'), ('Verona', 'Fiorentina'),
    ('Lecce', 'Atalanta'), ('Inter', 'Roma'), ('Sassuolo', 'Cagliari'), ('Udinese', 'Como'),
    ('Pisa', 'Torino'), ('Juventus', 'Genoa'),

    # Matchday 32
    ('Atalanta', 'Juventus'), ('Bologna', 'Lecce'), ('Parma', 'Napoli'), ('Genoa', 'Sassuolo'),
    ('Torino', 'Verona'), ('Milan', 'Udinese'), ('Cagliari', 'Cremonese'), ('Como', 'Inter'),
    ('Roma', 'Pisa'), ('Fiorentina', 'Lazio'),

    # Matchday 33
    ('Udinese', 'Parma'), ('Inter', 'Cagliari'), ('Cremonese', 'Torino'), ('Pisa', 'Genoa'),
    ('Juventus', 'Bologna'), ('Sassuolo', 'Como'), ('Roma', 'Atalanta'), ('Napoli', 'Lazio'),
    ('Lecce', 'Fiorentina'), ('Verona', 'Milan'),

    # Matchday 34
    ('Genoa', 'Como'), ('Lazio', 'Udinese'), ('Milan', 'Juventus'), ('Torino', 'Inter'),
    ('Bologna', 'Roma'), ('Parma', 'Pisa'), ('Fiorentina', 'Sassuolo'), ('Verona', 'Lecce'),
    ('Napoli', 'Cremonese'), ('Cagliari', 'Atalanta'),

    # Matchday 35
    ('Udinese', 'Torino'), ('Juventus', 'Verona'), ('Atalanta', 'Genoa'), ('Cremonese', 'Lazio'),
    ('Como', 'Napoli'), ('Bologna', 'Cagliari'), ('Pisa', 'Lecce'), ('Inter', 'Parma'),
    ('Roma', 'Fiorentina'), ('Sassuolo', 'Milan'),

    # Matchday 36
    ('Cagliari', 'Udinese'), ('Fiorentina', 'Genoa'), ('Verona', 'Como'), ('Milan', 'Atalanta'),
    ('Lecce', 'Juventus'), ('Lazio', 'Inter'), ('Napoli', 'Bologna'), ('Cremonese', 'Pisa'),
    ('Parma', 'Roma'), ('Torino', 'Sassuolo'),

    # Matchday 37
    ('Udinese', 'Cremonese'), ('Pisa', 'Napoli'), ('Como', 'Parma'), ('Sassuolo', 'Lecce'),
    ('Inter', 'Verona'), ('Atalanta', 'Bologna'), ('Genoa', 'Milan'), ('Roma', 'Lazio'),
    ('Juventus', 'Fiorentina'), ('Cagliari', 'Torino'),

    # Matchday 38
    ('Napoli', 'Udinese'), ('Parma', 'Sassuolo'), ('Fiorentina', 'Atalanta'), ('Verona', 'Roma'),
    ('Lecce', 'Genoa'), ('Lazio', 'Pisa'), ('Milan', 'Cagliari'), ('Bologna', 'Inter'),
    ('Torino', 'Juventus'), ('Cremonese', 'Como'),
]


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_relegation_zone_teams(min_points: int = 40) -> List[str]:
    """
    Get list of teams that could realistically be relegated.

    Args:
        min_points: Points threshold above which teams are considered safe

    Returns:
        List of team names below the threshold
    """
    return [team for team, stats in TEAMS_DATA.items() if stats['Pts'] <= min_points]


def get_form_string(team: str) -> str:
    """
    Convert form data to string representation (W/D/L).

    Args:
        team: Team name

    Returns:
        String like "W D L L W"
    """
    if team not in LAST_5_PERFORMANCE:
        return "N/A"

    return " ".join([
        "W" if r == 3 else "D" if r == 1 else "L"
        for r in LAST_5_PERFORMANCE[team]
    ])


def get_form_points(team: str) -> int:
    """
    Get total points from last 5 games.

    Args:
        team: Team name

    Returns:
        Total points (0-15)
    """
    if team not in LAST_5_PERFORMANCE:
        return 0
    return sum(LAST_5_PERFORMANCE[team])


# ==========================================
# LIVE DATA LOADING
# ==========================================

def _load_data_from_api() -> bool:
    """
    Attempt to load data from the Football API.

    Returns:
        True if successful, False otherwise
    """
    global _teams_data, _last_5_performance, _fixtures, _data_source, TEAMS_DATA, LAST_5_PERFORMANCE, FIXTURES

    try:
        from api_client import load_live_data, apply_name_mapping

        teams, form, fixtures = load_live_data()
        teams, form, fixtures = apply_name_mapping(teams, form, fixtures)

        # Update module-level variables
        _teams_data = teams
        _last_5_performance = form
        _fixtures = fixtures

        # Also update the exported constants for backward compatibility
        TEAMS_DATA.clear()
        TEAMS_DATA.update(teams)

        LAST_5_PERFORMANCE.clear()
        LAST_5_PERFORMANCE.update(form)

        FIXTURES.clear()
        FIXTURES.extend(fixtures)

        _data_source = "live API"
        logger.info(f"Loaded live data: {len(teams)} teams, {len(fixtures)} fixtures")
        return True

    except ImportError as e:
        logger.warning(f"API client not available: {e}")
        return False
    except ValueError as e:
        logger.warning(f"API configuration error: {e}")
        return False
    except Exception as e:
        logger.warning(f"Failed to load from API: {e}")
        return False


def _use_static_data() -> None:
    """Use the static data defined in this module."""
    global _teams_data, _last_5_performance, _fixtures, _data_source

    _teams_data = TEAMS_DATA.copy()
    _last_5_performance = {k: v.copy() for k, v in LAST_5_PERFORMANCE.items()}
    _fixtures = FIXTURES.copy()
    _data_source = "static fallback"
    logger.info("Using static fallback data")


def load_data(force_refresh: bool = False) -> Tuple[Dict[str, Dict[str, int]], Dict[str, List[int]], List[Tuple[str, str]]]:
    """
    Load team data, form, and fixtures.

    Attempts to load from API first, falls back to static data if unavailable.

    Args:
        force_refresh: If True, reload data even if already cached

    Returns:
        Tuple of (teams_data, form_data, fixtures)
    """
    global _teams_data, _last_5_performance, _fixtures

    # Return cached data if available
    if not force_refresh and _teams_data is not None:
        return _teams_data, _last_5_performance, _fixtures

    # Try API first (unless explicitly disabled)
    if not USE_STATIC_DATA:
        api_key = os.environ.get("FOOTBALL_API_KEY")
        if api_key:
            if _load_data_from_api():
                return _teams_data, _last_5_performance, _fixtures

    # Fall back to static data
    _use_static_data()
    return _teams_data, _last_5_performance, _fixtures


def get_data_source() -> str:
    """
    Get the current data source.

    Returns:
        String describing the data source ("live API", "static fallback", or "not loaded")
    """
    return _data_source


def is_using_live_data() -> bool:
    """
    Check if currently using live API data.

    Returns:
        True if using live data, False otherwise
    """
    return _data_source == "live API"


