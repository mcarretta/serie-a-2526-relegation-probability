# Serie A Relegation Monte Carlo Simulator

This project provides a parallelized Monte Carlo simulation engine designed to estimate relegation probabilities for Serie A teams as of Matchday 24. It moves beyond simple win/loss ratios by simulating individual match scores based on offensive/defensive strength, recent form, and stochastic "chaos" factors.

P.S. Sempre Forza Parma 💛💙

---

## 1. Statistical Core: Poisson Distribution

The simulator treats every match as a set of independent events. The number of goals scored by a team is modeled using a **Poisson distribution**, which is the industry standard for modeling low-frequency events like football goals.

For each match, an Expected Goals ($xG$) value ($\lambda$) is calculated for the Home and Away teams. The probability of a team scoring exactly $k$ goals is:

$$
P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

---

## 2. Team Strength Ratings

The engine calculates base ratings by comparing a team's performance to the league average across 24 matches.

### Base Attack and Defense

Base strength is normalized such that **1.0** represents the league average.

- **Attack Strength ($Att$):**
  $$
  \frac{\text{Goals Scored} / \text{Games Played}}{\text{League Avg Goals Scored} / \text{Games Played}}
  $$
- **Defense Strength ($Def$):**
  $$
  \frac{\text{Goals Conceded} / \text{Games Played}}{\text{League Avg Goals Conceded} / \text{Games Played}}
  $$

### Recent Form Adjustment

The model applies a Bayesian-style update using the **Last 5 Matches** to account for momentum. It blends the season-long PPG with the recent PPG using a 70/30 weighting:

$$
\text{Form Multiplier} = 0.7 + 0.3 \times \left( \frac{\text{Recent PPG}}{\text{Season PPG}} \right)
$$

This multiplier is then used to "boost" the attack and "tighten" the defense (where a lower $Def$ value is superior):

$$
\text{Adjusted Att} = Att \times \text{Multiplier}
$$
$$
\text{Adjusted Def} = Def \times \frac{1}{\text{Multiplier}}
$$

---

## 3. Match Simulation Logic

For every fixture $(H, A)$, the expected goals for the Home team ($\lambda_H$) and Away team ($\lambda_A$) are calculated as follows:

$$
\lambda_H = Att_H \times Def_A \times \text{AvgGoals}_{\text{home}} \times \text{HomeAdvantage} \times \text{Chaos}_H
$$
$$
\lambda_A = Att_A \times Def_H \times \text{AvgGoals}_{\text{away}} \times \text{Chaos}_A
$$

- **Home Advantage:** A constant multiplier (default 1.15) reflecting the statistical edge of playing at home.
- **Chaos Factor:** A random variable $\sim \text{Uniform}(1 - c, 1 + c)$ that injects volatility into every match, allowing for "Any Given Sunday" upsets.

---

## 4. Simulation Execution

- The model runs **100,000 independent "parallel universes"** using Python's multiprocessing to handle the heavy computational load.
- **Tie-breaking:** The simulation generates actual scores, allowing the final table to be sorted by Points first, then Goal Difference ($GD$), mirroring real Serie A rules.
- **Probability Calculation:**

$$
P(\text{Relegation}) = \frac{\sum \text{Simulations ending in bottom 3}}{\text{Total Simulations}} \times 100
$$

---

## Features

- Parallelized for speed (uses all CPU cores)
- Realistic match simulation (Poisson, home advantage, chaos)
- Team strength and recent form incorporated
- Outputs relegation probabilities for all teams (except those already safe)

---

## Usage

1. Install requirements (see `requirements.txt` if provided)
2. Run the main script:
   ```bash
   python relegation_proba_with_strength.py
   ```
3. View the output table for relegation probabilities.

---

