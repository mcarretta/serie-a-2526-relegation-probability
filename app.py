"""
Serie A 2025/26 Relegation Probability - Streamlit Web App

A Monte Carlo simulation tool for predicting Serie A relegation probabilities.
"""

import streamlit as st
import pandas as pd

from simulation import run_simulation, get_risk_status, get_available_cpus
from data import (
    TEAMS_DATA,
    FIXTURES,
    LAST_5_PERFORMANCE,
    get_relegation_zone_teams,
    get_form_string,
    get_form_points,
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Serie A 2025/26 Relegation Probabilities",
    page_icon="⚽",
    layout="centered",  # Changed from "wide" for better mobile support
    initial_sidebar_state="collapsed"  # Collapsed by default on mobile
)

# Mobile-friendly CSS with iOS Safari specific fixes
st.markdown("""
    <style>
    /* Base mobile responsiveness */
    .main .block-container {
        max-width: 100%;
        padding: 1rem;
    }
    
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            min-height: 44px;
        }
        .element-container {
            width: 100%;
        }
        /* Prevent zoom on iOS */
        input, select, textarea, button {
            font-size: 16px !important;
        }
        /* Fix dataframe overflow */
        [data-testid="stDataFrame"] {
            width: 100%;
            overflow-x: auto;
        }
    }
    
    /* iOS Safari specific fixes */
    @supports (-webkit-touch-callout: none) {
        .main {
            min-height: -webkit-fill-available;
        }
    }
    
    /* Improve touch targets */
    button, a, [role="button"] {
        min-height: 44px;
        min-width: 44px;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

def render_sidebar() -> tuple[float, int, bool, int]:
    """Render sidebar controls and return settings."""
    st.sidebar.header("⚙️ Simulation Settings")

    chaos_factor = st.sidebar.slider(
        "Chaos Factor",
        min_value=0.0,
        max_value=0.5,
        value=0.25,
        step=0.05,
        help="Random performance fluctuation per match. Higher = more unpredictable results."
    )

    n_simulations = st.sidebar.select_slider(
        "Number of Simulations",
        options=[1000, 5000, 10000, 25000, 50000, 100000],
        value=10000,
        help="More simulations = more stable probabilities, but slower."
    )

    include_form = st.sidebar.checkbox(
        "Include Recent Form",
        value=True,
        help="Weight recent 5-game performance in predictions."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🖥️ Performance")

    available_cpus = get_available_cpus()
    n_workers = st.sidebar.slider(
        "CPU Workers",
        min_value=1,
        max_value=available_cpus,
        value=available_cpus,
        help=f"Number of CPU cores to use for parallel simulation. Your system has {available_cpus} cores."
    )

    st.sidebar.markdown("---")
    render_standings_sidebar()

    return chaos_factor, n_simulations, include_form, n_workers


def render_standings_sidebar():
    """Render current standings in sidebar."""
    st.sidebar.markdown("### 📊 Current Standings")

    standings_df = pd.DataFrame([
        {"Team": team, "Pts": data["Pts"], "GF": data["GF"], "GA": data["GA"]}
        for team, data in TEAMS_DATA.items()
    ]).sort_values("Pts", ascending=False).reset_index(drop=True)

    standings_df.index = standings_df.index + 1
    # Use smaller height on mobile for better performance
    st.sidebar.dataframe(standings_df, use_container_width=True, height=350)


# ==========================================
# MAIN CONTENT
# ==========================================

def render_header(chaos_factor: float, n_simulations: int, include_form: bool, n_workers: int):
    """Render main content header."""
    # Use responsive columns that stack on mobile
    col1, col2 = st.columns([2, 1], gap="medium")

    with col1:
        st.subheader("🎲 Run Simulation")
        st.markdown(f"""
        **Current Settings:**
        - Chaos Factor: **{chaos_factor * 100:.0f}%**
        - Simulations: **{n_simulations:,}**
        - Recent Form: **{'Included' if include_form else 'Not Included'}**
        - CPU Workers: **{n_workers}** cores
        """)

    with col2:
        st.subheader("📅 Remaining Matches")
        st.metric("Fixtures to Play", len(FIXTURES))


def render_form_table():
    """Render recent form table for relegation zone teams."""
    st.subheader("📈 Recent Form (Last 5 Games)")

    form_data = []
    for team in get_relegation_zone_teams():
        form_data.append({
            "Team": team,
            "Last 5 Results": get_form_string(team),
            "Points (Last 5)": get_form_points(team),
            "PPG (Last 5)": get_form_points(team) / 5
        })

    form_df = pd.DataFrame(form_data).sort_values(
        "Points (Last 5)", ascending=False
    ).reset_index(drop=True)

    st.dataframe(form_df, use_container_width=True, hide_index=True)


def highlight_status(row) -> list[str]:
    """Apply row highlighting based on risk status."""
    status = row["Status"]

    if "CRITICAL" in status:
        return ["background-color: #ffcccc"] * len(row)
    elif "HIGH RISK" in status:
        return ["background-color: #ffe6cc"] * len(row)
    elif "AT RISK" in status:
        return ["background-color: #fff2cc"] * len(row)
    elif "UNSAFE" in status:
        return ["background-color: #ffffcc"] * len(row)
    else:
        return ["background-color: #ccffcc"] * len(row)


def render_results(
    results_baseline: dict,
    results_form: dict,
    n_simulations: int,
    include_form: bool
):
    """Render simulation results."""
    st.success("✅ Simulation complete!")
    st.markdown("---")

    # Prepare results dataframe
    excluded_teams = [
        team for team, stats in TEAMS_DATA.items()
        if stats['Pts'] > 40
    ]

    results_data = []
    for team in TEAMS_DATA:
        if team in excluded_teams:
            continue

        baseline_prob = (results_baseline[team] / n_simulations) * 100
        form_prob = (results_form[team] / n_simulations) * 100
        change = form_prob - baseline_prob

        if form_prob > 0.01 or baseline_prob > 0.01:
            results_data.append({
                "Team": team,
                "Current Pts": TEAMS_DATA[team]["Pts"],
                "Baseline %": baseline_prob,
                "With Form %": form_prob if include_form else baseline_prob,
                "Change %": change if include_form else 0,
                "Status": get_risk_status(form_prob)
            })

    results_df = pd.DataFrame(results_data)
    results_df = results_df.sort_values(
        "With Form %", ascending=False
    ).reset_index(drop=True)

    # Display results table
    st.subheader("📉 Relegation Probabilities")

    styled_df = results_df.style.apply(highlight_status, axis=1).format({
        "Baseline %": "{:.2f}%",
        "With Form %": "{:.2f}%",
        "Change %": "{:+.2f}%"
    })

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Visualization
    st.subheader("📊 Probability Distribution")
    chart_data = results_df[["Team", "With Form %"]].set_index("Team")
    st.bar_chart(chart_data, color="#ff6b6b")

    # Key insights
    render_insights(results_df)


def render_insights(results_df: pd.DataFrame):
    """Render key insights metrics."""
    st.subheader("🔍 Key Insights")

    most_likely = results_df.iloc[0]
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.metric(
            "Most Likely to Relegate",
            most_likely["Team"],
            f"{most_likely['With Form %']:.1f}%"
        )

    with col2:
        critical_teams = results_df[results_df["With Form %"] > 50]
        st.metric(
            "Teams in Danger Zone",
            f"{len(critical_teams)} teams",
            "> 50% chance"
        )

    with col3:
        safe_teams = results_df[results_df["With Form %"] < 5]
        st.metric(
            "Relatively Safe",
            f"{len(safe_teams)} teams",
            "< 5% chance"
        )


# ==========================================
# MAIN APP
# ==========================================

def main():
    """Main application entry point."""
    st.title("⚽ Serie A 2025/26 Relegation Probabilities")
    st.markdown("**Monte Carlo Simulation Engine**")
    st.markdown("---")

    # Sidebar
    chaos_factor, n_simulations, include_form, n_workers = render_sidebar()

    # Main content header
    render_header(chaos_factor, n_simulations, include_form, n_workers)

    # Run simulation button
    if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
        with st.spinner(f"Running {n_simulations:,} simulations on {n_workers} CPU cores..."):
            progress_bar = st.progress(0)

            # Run baseline simulation
            progress_bar.progress(25)
            results_baseline = run_simulation(
                TEAMS_DATA, FIXTURES, chaos_factor,
                form_data=None, n_sims=n_simulations,
                use_parallel=True, n_workers=n_workers
            )

            progress_bar.progress(75)

            # Run with form if enabled
            if include_form:
                results_form = run_simulation(
                    TEAMS_DATA, FIXTURES, chaos_factor,
                    form_data=LAST_5_PERFORMANCE, n_sims=n_simulations,
                    use_parallel=True, n_workers=n_workers
                )
            else:
                results_form = results_baseline

            progress_bar.progress(100)

        render_results(results_baseline, results_form, n_simulations, include_form)
    else:
        st.info("👆 Click the button above to run the Monte Carlo simulation and see relegation probabilities.")

        if include_form:
            render_form_table()

    # Footer
    st.markdown("---")
    st.markdown("*Simulation based on Monte Carlo method using Poisson distribution for goal scoring.*")


if __name__ == "__main__":
    main()
