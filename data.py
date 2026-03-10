"""
Serie A 2025/26 Season Data

This module contains all the team data, fixtures, and form information
for the Serie A 2025/26 season simulation.
"""

from typing import Dict, List, Tuple

# ==========================================
# TEAM DATA
# ==========================================

# Points, Goals For (GF), Goals Against (GA) after 28 matchdays
TEAMS_DATA: Dict[str, Dict[str, int]] = {
    # Sorted by points (descending)
    'Inter': {'Pts': 67, 'GF': 64, 'GA': 22},
    'Milan': {'Pts': 60, 'GF': 44, 'GA': 20},
    'Napoli': {'Pts': 56, 'GF': 43, 'GA': 29},
    'Como': {'Pts': 51, 'GF': 46, 'GA': 21},
    'Roma': {'Pts': 51, 'GF': 38, 'GA': 21},
    'Juventus': {'Pts': 50, 'GF': 50, 'GA': 28},
    'Atalanta': {'Pts': 46, 'GF': 39, 'GA': 26},
    'Bologna': {'Pts': 39, 'GF': 37, 'GA': 34},
    'Sassuolo': {'Pts': 38, 'GF': 35, 'GA': 38},
    'Lazio': {'Pts': 37, 'GF': 28, 'GA': 28},
    'Udinese': {'Pts': 36, 'GF': 33, 'GA': 41},
    'Parma': {'Pts': 34, 'GF': 20, 'GA': 32},
    'Torino': {'Pts': 30, 'GF': 28, 'GA': 49},
    'Cagliari': {'Pts': 30, 'GF': 30, 'GA': 38},
    'Genoa': {'Pts': 30, 'GF': 34, 'GA': 40},
    'Lecce': {'Pts': 27, 'GF': 20, 'GA': 37},
    'Fiorentina': {'Pts': 25, 'GF': 21, 'GA': 38},
    'Cremonese': {'Pts': 24, 'GF': 22, 'GA': 40},
    'Verona': {'Pts': 18, 'GF': 22, 'GA': 49},
    'Pisa': {'Pts': 15, 'GF': 20, 'GA': 48},
}


# ==========================================
# RECENT FORM
# ==========================================

# Points earned in last 5 games (3=Win, 1=Draw, 0=Loss)
LAST_5_PERFORMANCE: Dict[str, List[int]] = {
    'Inter': [3, 3, 3, 3, 0],       # L (0-1 vs Milan)
    'Milan': [3, 1, 0, 3, 3],        # W (1-0 vs Inter)
    'Napoli': [3, 1, 0, 3, 3],       # W (2-1 vs Torino)
    'Roma': [3, 1, 3, 1, 0],         # L (1-2 vs Genoa)
    'Como': [0, 1, 3, 3, 3],         # W (2-1 vs Cagliari)
    'Juventus': [1, 0, 0, 1, 3],     # W (4-0 vs Pisa)
    'Atalanta': [3, 3, 3, 0, 1],     # D (2-2 vs Udinese)
    'Bologna': [0, 3, 3, 3, 0],      # L (1-2 vs Verona)
    'Sassuolo': [0, 3, 3, 3, 0],     # L (1-2 vs Lazio)
    'Udinese': [0, 0, 0, 3, 1],      # D (2-2 vs Atalanta)
    'Lazio': [1, 0, 1, 0, 3],        # W (2-1 vs Sassuolo)
    'Parma': [3, 3, 3, 1, 1],        # D (0-0 vs Fiorentina)
    'Torino': [1, 0, 0, 3, 0],       # L (1-2 vs Napoli)
    'Cagliari': [0, 0, 1, 1, 0],     # L (1-2 vs Como)
    'Genoa': [0, 1, 3, 0, 3],        # W (2-1 vs Roma)
    'Cremonese': [0, 1, 0, 0, 0],    # L (1-2 vs Lecce)
    'Fiorentina': [1, 3, 3, 0, 1],   # D (0-0 vs Parma)
    'Lecce': [3, 3, 0, 0, 3],        # W (2-1 vs Cremonese)
    'Pisa': [1, 0, 0, 0, 0],         # L (0-4 vs Juventus)
    'Verona': [1, 0, 0, 0, 3],       # W (2-1 vs Bologna)
}


# ==========================================
# REMAINING FIXTURES
# ==========================================

# Remaining fixtures from Matchday 29 to 38
FIXTURES: List[Tuple[str, str]] = [


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

