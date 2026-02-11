import numpy as np
from multiprocessing import Pool, cpu_count

# ==========================================
# 1. CONFIGURATION & DATA
# ==========================================

# Simulation Settings
N_SIMULATIONS = 100000  # Higher number = more stable probabilities
CHAOS_FACTOR = 0.25  # +/- 25% random performance fluctuation per match (Realism)
HOME_ADVANTAGE = 1.15  # Home teams score 15% more goals on average

# League Averages (approximate for Serie A)
AVG_GOALS_HOME = 1.45
AVG_GOALS_AWAY = 1.15

# TEAM DATA: Points, Goals For (GF), Goals Against (GA)
teams_data = {
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
    # --- The Top/Mid Table  ---
    'Inter': {'Pts': 58, 'GF': 57, 'GA': 19},
    'Milan': {'Pts': 50, 'GF': 38, 'GA': 17},
    'Napoli': {'Pts': 49, 'GF': 36, 'GA': 23},
    'Juventus': {'Pts': 46, 'GF': 41, 'GA': 20},
    'Roma': {'Pts': 46, 'GF': 29, 'GA': 14},
    'Como': {'Pts': 41, 'GF': 37, 'GA': 16},
    'Atalanta': {'Pts': 39, 'GF': 32, 'GA': 21},
}

# RECENT FORM: Points earned in last 5 games (List format to calc average)
last_5_performance = {
    'Inter': [3, 3, 3, 3, 3], 'Napoli': [1, 3, 0, 3, 3], 'Milan': [1, 3, 3, 1, 3],
    'Juventus': [3, 0, 3, 3, 1], 'Atalanta': [3, 1, 3, 1, 3], 'Roma': [3, 3, 1, 0, 3],
    'Como': [1, 0, 3, 3, 1], 'Lazio': [3, 0, 1, 3, 1], 'Udinese': [1, 0, 3, 3, 0],
    'Bologna': [3, 0, 0, 0, 0], 'Sassuolo': [0, 0, 3, 3, 0], 'Cagliari': [0, 3, 3, 3, 0],
    'Torino': [0, 0, 0, 3, 1], 'Parma': [1, 1, 0, 0, 3], 'Genoa': [3, 1, 3, 0, 0],
    'Cremonese': [0, 1, 0, 0, 0], 'Lecce': [0, 0, 1, 0, 3], 'Fiorentina': [1, 3, 0, 0, 1],
    'Pisa': [1, 1, 0, 0, 1], 'Verona': [0, 1, 0, 0, 1]
}

# REMAINING FIXTURES (Matchday 25 - 38)
fixtures = [
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
    ('Torino', 'Juventus'), ('Cremonese', 'Como')
]


# ==========================================
# 2. SIMULATION ENGINE
# ==========================================

def get_team_ratings(data, form_data=None):
    """Calculates Attack and Defense strength relative to league average."""
    ratings = {}
    league_avg_gf = np.mean([t['GF'] for t in data.values()])
    league_avg_ga = np.mean([t['GA'] for t in data.values()])

    for team, stats in data.items():
        # Base Ratings (1.0 = League Average)
        # Using 24 games played for normalization
        att = (stats['GF'] / 24) / (league_avg_gf / 24)
        dfe = (stats['GA'] / 24) / (league_avg_ga / 24)

        # Apply Recent Form (if provided)
        # Logic: Weighted average of Season Performance (70%) + Recent Form (30%)
        if form_data and team in form_data:
            recent_points = sum(form_data[team])
            recent_ppg = recent_points / 5.0
            season_ppg = stats['Pts'] / 24.0

            if season_ppg > 0:
                # Calculate a multiplier. If recent PPG > Season PPG, multiplier > 1.0
                form_multiplier = 0.7 + 0.3 * (recent_ppg / season_ppg)

                # Boost attack, improve defense (lower is better for defense rating)
                att *= form_multiplier
                dfe *= (1.0 / form_multiplier)

        ratings[team] = {'Att': att, 'Def': dfe}
    return ratings


def simulate_single_season(args):
    """Run a single season simulation. Designed to be called in parallel."""
    data, fixtures_list, team_ratings, seed = args

    np.random.seed(seed)

    # Create a fresh table for this simulation run
    sim_table = {t: {'Pts': data[t]['Pts'], 'GD': data[t]['GF'] - data[t]['GA']} for t in data}

    for home, away in fixtures_list:
        # 1. Get Base Strengths
        h_att = team_ratings[home]['Att']
        h_def = team_ratings[home]['Def']
        a_att = team_ratings[away]['Att']
        a_def = team_ratings[away]['Def']

        # 2. Apply Chaos Factor (Random volatility per match)
        h_chaos = np.random.uniform(1.0 - CHAOS_FACTOR, 1.0 + CHAOS_FACTOR)
        a_chaos = np.random.uniform(1.0 - CHAOS_FACTOR, 1.0 + CHAOS_FACTOR)

        # 3. Calculate Expected Goals
        h_exp_goals = h_att * a_def * AVG_GOALS_HOME * h_chaos
        a_exp_goals = a_att * h_def * AVG_GOALS_AWAY * a_chaos

        # 4. Simulate Actual Score (Poisson Distribution)
        h_score = np.random.poisson(h_exp_goals)
        a_score = np.random.poisson(a_exp_goals)

        # 5. Update Standings
        if h_score > a_score:
            sim_table[home]['Pts'] += 3
        elif a_score > h_score:
            sim_table[away]['Pts'] += 3
        else:
            sim_table[home]['Pts'] += 1
            sim_table[away]['Pts'] += 1

        sim_table[home]['GD'] += (h_score - a_score)
        sim_table[away]['GD'] += (a_score - h_score)

    # End of Season: Sort table
    sorted_table = sorted(sim_table.items(), key=lambda x: (x[1]['Pts'], x[1]['GD']), reverse=True)

    # Identify Relegated Teams (Bottom 3)
    relegated_teams = [t[0] for t in sorted_table[-3:]]
    return relegated_teams


def run_season_simulation(data, fixtures_list, form_data=None, n_sims=1000, n_processes=None):
    """Run parallel Monte Carlo simulation of remaining season."""
    if n_processes is None:
        n_processes = cpu_count()

    relegation_counts = {t: 0 for t in data}
    team_ratings = get_team_ratings(data, form_data)

    # Prepare arguments for parallel processing
    # Each simulation gets a unique seed for reproducibility
    args_list = [
        (data, fixtures_list, team_ratings, 42 + i)
        for i in range(n_sims)
    ]

    # Run simulations in parallel
    with Pool(processes=n_processes) as pool:
        results = pool.map(simulate_single_season, args_list)

    # Aggregate results
    for relegated_teams in results:
        for team in relegated_teams:
            relegation_counts[team] += 1

    return relegation_counts


# ==========================================
# 3. EXECUTION
# ==========================================

if __name__ == '__main__':
    n_cpus = cpu_count()
    print(f"Running {N_SIMULATIONS} simulations with Chaos Factor: {CHAOS_FACTOR * 100}%...")
    print(f"Using {n_cpus} CPU cores for parallel processing...")

    # Run 1: Baseline (Purely based on season-long stats)
    print("\n[1/2] Running baseline simulation...")
    results_baseline = run_season_simulation(teams_data, fixtures, form_data=None, n_sims=N_SIMULATIONS)

    # Run 2: With Form (Heavily weighted by last 5 games)
    print("[2/2] Running simulation with form data...")
    results_form = run_season_simulation(teams_data, fixtures, form_data=last_5_performance, n_sims=N_SIMULATIONS)

    # ==========================================
    # 4. OUTPUT FORMATTING
    # ==========================================

    # Identify teams with more than 40 points
    excluded_teams = [team for team, stats in teams_data.items() if stats['Pts'] > 40]

    print("\nRELEGATION PROBABILITIES (End of Season Projection)")
    print("=" * 75)
    print(f"{'TEAM':<15} | {'BASELINE':<12} | {'WITH FORM':<12} | {'CHANGE':<10} | {'STATUS'}")
    print("-" * 75)

    # Sort by "With Form" probability
    sorted_results = sorted(results_form.items(), key=lambda x: x[1], reverse=True)

    for team, form_count in sorted_results:
        if team in excluded_teams:
            continue  # Skip teams with more than 40 points

        baseline_prob = (results_baseline[team] / N_SIMULATIONS) * 100
        form_prob = (form_count / N_SIMULATIONS) * 100
        change = form_prob - baseline_prob

        # Define status label
        if form_prob > 90:
            status = "🚨 CRITICAL"
        elif form_prob > 50:
            status = "⚠️ HIGH RISK"
        elif form_prob > 20:
            status = "🟠 AT RISK"
        elif form_prob > 5:
            status = "🟡 UNSAFE"
        else:
            status = "🟢 SAFE"

        # Only show teams with >0.1% chance to keep table clean
        if form_prob > 0.01 or baseline_prob > 0.01:
            print(f"{team:<15} | {baseline_prob:>11.2f}% | {form_prob:>11.2f}% | {change:>+9.2f}% | {status}")

    print("=" * 75)
