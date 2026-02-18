"""
Serie A 2025/26 Season Data

This module contains all the team data, fixtures, and form information
for the Serie A 2025/26 season simulation.
"""

from typing import Dict, List, Tuple

# ==========================================
# TEAM DATA
# ==========================================

# Points, Goals For (GF), Goals Against (GA) after 25 matchdays
TEAMS_DATA: Dict[str, Dict[str, int]] = {
    # Sorted by points (descending)
    'Inter': {'Pts': 61, 'GF': 60, 'GA': 21},
    'Milan': {'Pts': 54, 'GF': 41, 'GA': 19},
    'Napoli': {'Pts': 50, 'GF': 38, 'GA': 25},
    'Roma': {'Pts': 47, 'GF': 31, 'GA': 27},
    'Juventus': {'Pts': 46, 'GF': 43, 'GA': 22},
    'Atalanta': {'Pts': 42, 'GF': 34, 'GA': 23},
    'Como': {'Pts': 42, 'GF': 39, 'GA': 19},
    'Bologna': {'Pts': 33, 'GF': 34, 'GA': 32},
    'Lazio': {'Pts': 33, 'GF': 26, 'GA': 25},
    'Sassuolo': {'Pts': 32, 'GF': 29, 'GA': 37},
    'Udinese': {'Pts': 32, 'GF': 28, 'GA': 38},
    'Parma': {'Pts': 29, 'GF': 18, 'GA': 31},
    'Cagliari': {'Pts': 28, 'GF': 28, 'GA': 37},
    'Torino': {'Pts': 27, 'GF': 26, 'GA': 44},
    'Lecce': {'Pts': 24, 'GF': 19, 'GA': 31},
    'Cremonese': {'Pts': 24, 'GF': 21, 'GA': 33},
    'Genoa': {'Pts': 24, 'GF': 29, 'GA': 37},
    'Fiorentina': {'Pts': 21, 'GF': 31, 'GA': 39},
    'Pisa': {'Pts': 15, 'GF': 21, 'GA': 42},
    'Verona': {'Pts': 15, 'GF': 19, 'GA': 43},
}


# ==========================================
# RECENT FORM
# ==========================================

# Points earned in last 5 games (3=Win, 1=Draw, 0=Loss)
LAST_5_PERFORMANCE: Dict[str, List[int]] = {
    'Inter': [3, 3, 3, 3, 3],
    'Napoli': [3, 0, 3, 3, 1],
    'Milan': [3, 1, 3, 3, 1],
    'Juventus': [0, 3, 3, 1, 0],
    'Atalanta': [1, 3, 1, 3, 3],
    'Roma': [3, 1, 0, 3, 1],
    'Como': [3, 3, 1, 0, 1],
    'Lazio': [0, 1, 3, 1, 0],
    'Udinese': [0, 3, 3, 0, 0],
    'Bologna': [0, 0, 0, 0, 3],
    'Sassuolo': [0, 3, 3, 0, 3],
    'Cagliari': [3, 3, 3, 0, 0],
    'Torino': [0, 0, 3, 1, 0],
    'Parma': [1, 0, 0, 3, 3],
    'Genoa': [1, 3, 0, 0, 1],
    'Cremonese': [1, 0, 0, 0, 1],
    'Lecce': [0, 1, 0, 3, 3],
    'Fiorentina': [3, 0, 0, 1, 3],
    'Pisa': [1, 0, 0, 1, 0],
    'Verona': [1, 0, 0, 1, 0],
}


# ==========================================
# REMAINING FIXTURES
# ==========================================

# Remaining fixtures from Matchday 25 to 38
FIXTURES: List[Tuple[str, str]] = [
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

