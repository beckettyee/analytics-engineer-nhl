"""NHL Opponent & Schedule Intelligence Dashboard."""

import os
import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
from cryptography.hazmat.primitives import serialization


st.set_page_config(page_title="NHL Schedule Intelligence", layout="wide")


def _get_secret(key, default=""):
    """Get a config value from Streamlit secrets or environment variables."""
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, default)



@st.cache_resource
def get_connection():
    """Connect to Snowflake using key pair auth."""
    key_path = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH", "")
    if key_path and os.path.exists(key_path):
        with open(key_path, "rb") as f:
            pk = serialization.load_pem_private_key(f.read(), password=None)
    else:
        key_b64 = _get_secret("SNOWFLAKE_PRIVATE_KEY_B64")
        if key_b64:
            key_bytes = base64.b64decode(key_b64)
        else:
            key_data = _get_secret("SNOWFLAKE_PRIVATE_KEY")
            key_data = key_data.replace("\\n", "\n").strip()
            key_bytes = key_data.encode()
        pk = serialization.load_pem_private_key(key_bytes, password=None)

    private_key_bytes = pk.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return snowflake.connector.connect(
        account=_get_secret("SNOWFLAKE_ACCOUNT"),
        user=_get_secret("SNOWFLAKE_USER"),
        private_key=private_key_bytes,
        database=_get_secret("SNOWFLAKE_DATABASE", "NHL_ANALYTICS"),
        warehouse=_get_secret("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        schema="MART",
    )


@st.cache_data(ttl=600)
def load_data():
    """Load all mart tables into DataFrames."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ALTER WAREHOUSE COMPUTE_WH RESUME IF SUSPENDED")
    cur.close()
    games = pd.read_sql("SELECT * FROM fact_games", conn)
    teams = pd.read_sql("SELECT * FROM dim_teams", conn)
    dates = pd.read_sql("SELECT * FROM dim_dates", conn)
    venues = pd.read_sql("SELECT * FROM dim_venues", conn)
    return games, teams, dates, venues


def main():
    st.title("NHL Opponent & Schedule Intelligence")
    st.markdown("Interactive analytics for NHL game scheduling, demand drivers, and ticket pricing.")

    games, teams, dates, venues = load_data()

    # Normalize column names to lowercase
    games.columns = [c.lower() for c in games.columns]
    teams.columns = [c.lower() for c in teams.columns]
    dates.columns = [c.lower() for c in dates.columns]
    venues.columns = [c.lower() for c in venues.columns]

    # Enrich games with dimension data
    enriched = games.merge(
        teams.rename(columns={"team_id": "home_team_id", "team_name": "home_team_name", "short_name": "home_short_name", "conference": "home_conference"}),
        on="home_team_id", how="left"
    ).merge(
        teams.rename(columns={"team_id": "away_team_id", "team_name": "away_team_name", "short_name": "away_short_name"})[["away_team_id", "away_team_name", "away_short_name"]],
        on="away_team_id", how="left"
    ).merge(dates, on="date_id", how="left"
    ).merge(
        venues[["venue_id", "venue_name", "city", "state", "capacity"]],
        on="venue_id", how="left"
    )

    # --- Sidebar Filters ---
    st.sidebar.header("Filters")

    all_teams = sorted(teams["team_name"].dropna().unique())
    selected_teams = st.sidebar.multiselect("Teams", all_teams, default=[])

    season_stages = ["All"] + sorted(enriched["season_stage"].dropna().unique().tolist())
    selected_stage = st.sidebar.selectbox("Season Stage", season_stages)

    all_venues = sorted(enriched["venue_name"].dropna().unique())
    selected_venues = st.sidebar.multiselect("Venues", all_venues, default=[])

    # Apply filters
    filtered = enriched.copy()
    if selected_teams:
        filtered = filtered[
            (filtered["home_team_name"].isin(selected_teams)) |
            (filtered["away_team_name"].isin(selected_teams))
        ]
    if selected_stage != "All":
        filtered = filtered[filtered["season_stage"] == selected_stage]
    if selected_venues:
        filtered = filtered[filtered["venue_name"].isin(selected_venues)]

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["Schedule Overview", "Demand Analysis", "Pricing Strategy"])

    # --- Tab 1: Schedule Overview (Descriptive) ---
    with tab1:
        st.header("Schedule Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Games", len(filtered))
        col2.metric("Teams", filtered["home_team_name"].nunique())
        col3.metric("Venues", filtered["venue_name"].nunique())

        st.subheader("Games by Home Team")
        home_counts = filtered.groupby("home_team_name").size().reset_index(name="game_count").sort_values("game_count", ascending=False)
        fig1 = px.bar(home_counts, x="home_team_name", y="game_count", labels={"home_team_name": "Home Team", "game_count": "Games"})
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Games by Month")
        if "month_name" in filtered.columns and not filtered["month_name"].isna().all():
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthly = filtered.groupby("month_name").size().reset_index(name="game_count")
            monthly["month_name"] = pd.Categorical(monthly["month_name"], categories=month_order, ordered=True)
            monthly = monthly.sort_values("month_name")
            fig2 = px.bar(monthly, x="month_name", y="game_count", labels={"month_name": "Month", "game_count": "Games"})
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Game Schedule")
        display_cols = ["short_title", "datetime_local", "venue_name", "home_team_name", "away_team_name", "season_stage", "event_popularity"]
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols].sort_values("datetime_local", ascending=False), use_container_width=True)

    # --- Tab 2: Demand Analysis (Diagnostic) ---
    with tab2:
        st.header("Demand Analysis")
        st.markdown("What drives event popularity and demand?")

        st.subheader("Popularity by Home Team")
        team_pop = filtered.groupby("home_team_name")["event_popularity"].mean().reset_index().sort_values("event_popularity", ascending=False)
        fig3 = px.bar(team_pop, x="home_team_name", y="event_popularity", labels={"home_team_name": "Home Team", "event_popularity": "Avg Popularity"})
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Popularity by Day of Week")
        if "day_name" in filtered.columns and not filtered["day_name"].isna().all():
            day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            day_pop = filtered.groupby("day_name")["event_popularity"].mean().reset_index()
            day_pop["day_name"] = pd.Categorical(day_pop["day_name"], categories=day_order, ordered=True)
            day_pop = day_pop.sort_values("day_name")
            fig4 = px.bar(day_pop, x="day_name", y="event_popularity", labels={"day_name": "Day", "event_popularity": "Avg Popularity"})
            st.plotly_chart(fig4, use_container_width=True)

        st.subheader("Popularity vs Event Score")
        fig5 = px.scatter(filtered, x="event_score", y="event_popularity", hover_data=["short_title", "home_team_name"],
                          labels={"event_score": "Event Score", "event_popularity": "Popularity"})
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("Weekend vs Weekday Popularity")
        if "is_weekend" in filtered.columns:
            weekend_pop = filtered.groupby("is_weekend")["event_popularity"].mean().reset_index()
            weekend_pop["is_weekend"] = weekend_pop["is_weekend"].map({True: "Weekend", False: "Weekday"})
            fig6 = px.bar(weekend_pop, x="is_weekend", y="event_popularity", labels={"is_weekend": "", "event_popularity": "Avg Popularity"})
            st.plotly_chart(fig6, use_container_width=True)

    # --- Tab 3: Pricing Strategy (Diagnostic) ---
    with tab3:
        st.header("Pricing Strategy")
        st.markdown("Which games should be priced at a premium vs. discounted? Using demand signals (popularity, matchup score, timing) to recommend pricing tiers.")

        # Assign pricing tiers based on demand signals
        strategy = filtered.copy()
        strategy = strategy[strategy["event_popularity"].notna() & strategy["home_team_name"].notna()]

        if len(strategy) == 0:
            st.info("No games available for the current filter selection.")
        else:
            # Playoff vs Regular Season metrics
            playoff_count = len(strategy[strategy["season_stage"] == "postseason"])
            regular_count = len(strategy[strategy["season_stage"] != "postseason"])
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Games", len(strategy))
            col2.metric("Regular Season", regular_count)
            col3.metric("Playoff Games", playoff_count)

            # --- Playoff Round Demand Escalation ---
            st.subheader("Demand Escalation by Playoff Round")
            st.markdown("How much does demand increase as the playoffs progress?")

            def get_playoff_round(title):
                t = str(title).lower()
                if "stanley cup final" in t:
                    return "Stanley Cup Finals"
                elif "conference final" in t:
                    return "Conference Finals"
                elif "second round" in t:
                    return "Second Round"
                elif "first round" in t:
                    return "First Round"
                else:
                    return None

            playoff_games = strategy[strategy["season_stage"] == "postseason"].copy()
            if len(playoff_games) > 0:
                playoff_games["playoff_round"] = playoff_games["title"].apply(get_playoff_round)
                playoff_games = playoff_games[playoff_games["playoff_round"].notna()]

                if len(playoff_games) > 0:
                    round_order = ["First Round", "Second Round", "Conference Finals", "Stanley Cup Finals"]
                    round_stats = playoff_games.groupby("playoff_round").agg(
                        avg_popularity=("event_popularity", "mean"),
                        avg_score=("event_score", "mean"),
                        game_count=("game_id", "count")
                    ).reindex(round_order).dropna().reset_index()
                    round_stats.columns = ["Playoff Round", "Avg Popularity", "Avg Score", "Games"]

                    fig_round = px.bar(round_stats, x="Playoff Round", y="Avg Popularity",
                                       text="Games", color="Avg Score",
                                       color_continuous_scale=["#3498db", "#e74c3c"],
                                       labels={"Avg Popularity": "Avg Demand (Popularity)", "Avg Score": "Matchup Score"})
                    fig_round.update_traces(texttemplate="%{text} games", textposition="outside")
                    st.plotly_chart(fig_round, use_container_width=True)

                    # Regular season vs playoff comparison
                    reg_pop = strategy[strategy["season_stage"] != "postseason"]["event_popularity"].mean()
                    playoff_pop = playoff_games["event_popularity"].mean()
                    if reg_pop > 0:
                        lift = ((playoff_pop - reg_pop) / reg_pop) * 100
                        st.metric("Playoff Demand Lift vs Regular Season", f"+{lift:.0f}%",
                                  delta=f"{playoff_pop:.3f} vs {reg_pop:.3f} avg popularity")
                else:
                    st.info("No playoff round data available in current selection.")
            else:
                st.info("Filter to 'postseason' or 'All' to see playoff round analysis.")

            st.subheader("Regular Season vs Postseason Demand")
            stage_pop = strategy.groupby("season_stage")["event_popularity"].mean().reset_index()
            stage_pop["season_stage"] = stage_pop["season_stage"].fillna("Regular Season")
            stage_pop.columns = ["Stage", "Avg Popularity"]
            fig7 = px.bar(stage_pop, x="Stage", y="Avg Popularity",
                          color="Stage", color_discrete_map={"Regular Season": "#3498db", "postseason": "#e74c3c"},
                          labels={"Avg Popularity": "Avg Demand (Popularity)"})
            st.plotly_chart(fig7, use_container_width=True)

            st.subheader("Popularity vs Score — Playoff vs Regular Season")
            scatter_data = strategy.copy()
            scatter_data["stage_label"] = scatter_data["season_stage"].apply(
                lambda x: "Postseason" if x == "postseason" else "Regular Season"
            )
            fig8 = px.scatter(scatter_data, x="event_score", y="event_popularity", color="stage_label",
                              color_discrete_map={"Postseason": "#e74c3c", "Regular Season": "#3498db"},
                              hover_data=["short_title", "home_team_name"],
                              labels={"event_score": "Matchup Score", "event_popularity": "Demand (Popularity)", "stage_label": "Stage"})
            st.plotly_chart(fig8, use_container_width=True)

            st.subheader("Game-Level Detail")
            rec_cols = ["short_title", "datetime_local", "home_team_name", "venue_name", "event_popularity", "event_score", "season_stage"]
            available_rec = [c for c in rec_cols if c in strategy.columns]
            st.dataframe(strategy[available_rec].sort_values("event_popularity", ascending=False), use_container_width=True)


if __name__ == "__main__":
    main()
