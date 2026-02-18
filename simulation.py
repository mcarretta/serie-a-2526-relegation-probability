"""
Serie A Relegation Probability Simulation Engine

This module contains the Monte Carlo simulation logic for predicting
Serie A relegation probabilities using Poisson-based match simulation.
"""

import os
import numpy as np
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple, Optional

# ==========================================
# CONSTANTS
# ==========================================

AVG_GOALS_HOME = 1.45
AVG_GOALS_AWAY = 1.15


# ==========================================
# TEAM RATINGS
# ==========================================

def get_team_ratings(
    teams_data: Dict[str, Dict],
    form_data: Optional[Dict[str, List[int]]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Calculate Attack and Defense strength relative to league average.

    Args:
        teams_data: Dictionary with team stats (Pts, GF, GA)
        form_data: Optional dictionary with recent form (last 5 results)

    Returns:
        Dictionary mapping team names to their attack/defense ratings
    """
    ratings = {}
    league_avg_gf = np.mean([t['GF'] for t in teams_data.values()])
    league_avg_ga = np.mean([t['GA'] for t in teams_data.values()])

    for team, stats in teams_data.items():
        att = (stats['GF'] / 24) / (league_avg_gf / 24)
        dfe = (stats['GA'] / 24) / (league_avg_ga / 24)

        if form_data and team in form_data:
            recent_points = sum(form_data[team])
            recent_ppg = recent_points / 5.0
            season_ppg = stats['Pts'] / 24.0

            if season_ppg > 0:
                form_multiplier = 0.7 + 0.3 * (recent_ppg / season_ppg)
                att *= form_multiplier
                dfe *= (1.0 / form_multiplier)

        ratings[team] = {'Att': att, 'Def': dfe}

    return ratings


# ==========================================
# MATCH SIMULATION
# ==========================================

def simulate_match(
    home_team: str,
    away_team: str,
    team_ratings: Dict[str, Dict[str, float]],
    chaos_factor: float
) -> Tuple[int, int]:
    """
    Simulate a single match using Poisson distribution.

    Args:
        home_team: Name of the home team
        away_team: Name of the away team
        team_ratings: Team attack/defense ratings
        chaos_factor: Random performance fluctuation (0.0 - 0.5)

    Returns:
        Tuple of (home_score, away_score)
    """
    h_att = team_ratings[home_team]['Att']
    h_def = team_ratings[home_team]['Def']
    a_att = team_ratings[away_team]['Att']
    a_def = team_ratings[away_team]['Def']

    h_chaos = np.random.uniform(1.0 - chaos_factor, 1.0 + chaos_factor)
    a_chaos = np.random.uniform(1.0 - chaos_factor, 1.0 + chaos_factor)

    h_exp_goals = h_att * a_def * AVG_GOALS_HOME * h_chaos
    a_exp_goals = a_att * h_def * AVG_GOALS_AWAY * a_chaos

    h_score = np.random.poisson(h_exp_goals)
    a_score = np.random.poisson(a_exp_goals)

    return h_score, a_score


# ==========================================
# SEASON SIMULATION
# ==========================================

def simulate_single_season(args: Tuple) -> Tuple[List[str], Dict[str, int], int]:
    """
    Run a single season simulation.

    Args:
        args: Tuple of (teams_data, fixtures, team_ratings, chaos_factor, seed)

    Returns:
        Tuple of (relegated_teams, final_points_dict, min_safe_points)
    """
    data, fixtures_list, team_ratings, chaos_factor, seed = args

    np.random.seed(seed)

    sim_table = {
        t: {'Pts': data[t]['Pts'], 'GD': data[t]['GF'] - data[t]['GA']}
        for t in data
    }

    for home, away in fixtures_list:
        h_score, a_score = simulate_match(home, away, team_ratings, chaos_factor)

        if h_score > a_score:
            sim_table[home]['Pts'] += 3
        elif a_score > h_score:
            sim_table[away]['Pts'] += 3
        else:
            sim_table[home]['Pts'] += 1
            sim_table[away]['Pts'] += 1

        sim_table[home]['GD'] += (h_score - a_score)
        sim_table[away]['GD'] += (a_score - h_score)

    sorted_table = sorted(
        sim_table.items(),
        key=lambda x: (x[1]['Pts'], x[1]['GD']),
        reverse=True
    )
    relegated_teams = [t[0] for t in sorted_table[-3:]]

    # Get final points for each team
    final_points = {t: sim_table[t]['Pts'] for t in sim_table}

    # Min safe points = points of 17th place team (first non-relegated)
    min_safe_points = sorted_table[-4][1]['Pts']

    return relegated_teams, final_points, min_safe_points


def run_simulation(
    teams_data: Dict[str, Dict],
    fixtures: List[Tuple[str, str]],
    chaos_factor: float,
    form_data: Optional[Dict[str, List[int]]] = None,
    n_sims: int = 1000,
    base_seed: int = 42,
    use_parallel: bool = True,
    n_workers: Optional[int] = None
) -> Tuple[Dict[str, int], Dict[str, float], float]:
    """
    Run Monte Carlo simulation of remaining season.

    Args:
        teams_data: Dictionary with team stats (Pts, GF, GA)
        fixtures: List of remaining fixtures as (home, away) tuples
        chaos_factor: Random performance fluctuation (0.0 - 0.5)
        form_data: Optional dictionary with recent form data
        n_sims: Number of simulations to run
        base_seed: Base random seed for reproducibility
        use_parallel: Whether to use multiprocessing (default: True)
        n_workers: Number of worker processes (default: all CPUs)

    Returns:
        Tuple of:
        - Dictionary mapping team names to relegation counts
        - Dictionary mapping team names to average predicted points
        - Average minimum points to avoid relegation
    """
    relegation_counts = {t: 0 for t in teams_data}
    total_points = {t: 0 for t in teams_data}
    total_min_safe_points = 0
    team_ratings = get_team_ratings(teams_data, form_data)

    # Prepare arguments for all simulations
    sim_args = [
        (teams_data, fixtures, team_ratings, chaos_factor, base_seed + i)
        for i in range(n_sims)
    ]

    if use_parallel and n_sims >= 100:
        # Use multiprocessing for large simulation counts
        workers = n_workers or cpu_count()
        with Pool(processes=workers) as pool:
            results = pool.map(simulate_single_season, sim_args)

        for relegated_teams, final_points, min_safe_points in results:
            for team in relegated_teams:
                relegation_counts[team] += 1
            for team, pts in final_points.items():
                total_points[team] += pts
            total_min_safe_points += min_safe_points
    else:
        # Sequential processing for small simulation counts
        for args in sim_args:
            relegated_teams, final_points, min_safe_points = simulate_single_season(args)
            for team in relegated_teams:
                relegation_counts[team] += 1
            for team, pts in final_points.items():
                total_points[team] += pts
            total_min_safe_points += min_safe_points

    # Calculate averages
    avg_points = {t: total_points[t] / n_sims for t in teams_data}
    avg_min_safe_points = total_min_safe_points / n_sims

    return relegation_counts, avg_points, avg_min_safe_points


def get_available_cpus() -> int:
    """Get the number of available CPU cores."""
    return cpu_count()


def calculate_probabilities(
    relegation_counts: Dict[str, int],
    n_sims: int
) -> Dict[str, float]:
    """
    Convert relegation counts to probabilities.

    Args:
        relegation_counts: Dictionary mapping teams to relegation counts
        n_sims: Total number of simulations run

    Returns:
        Dictionary mapping team names to relegation probability (0-100)
    """
    return {
        team: (count / n_sims) * 100
        for team, count in relegation_counts.items()
    }


def get_risk_status(probability: float) -> str:
    """
    Determine risk status emoji based on relegation probability.

    Args:
        probability: Relegation probability (0-100)

    Returns:
        Status string with emoji
    """
    if probability > 90:
        return "🚨 CRITICAL"
    elif probability > 50:
        return "⚠️ HIGH RISK"
    elif probability > 20:
        return "🟠 AT RISK"
    elif probability > 5:
        return "🟡 UNSAFE"
    else:
        return "🟢 SAFE"

