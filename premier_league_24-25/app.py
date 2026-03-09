import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="PL Analytics 24/25", layout="wide", page_icon="⚽")

st.sidebar.title("⚽ PL Pro Analyzer")
page = st.sidebar.selectbox("Navigate:", ["Dashboard", "League Table", "Squad Analytics", "Live News" ])
BASE_URL = "http://127.0.0.1:8000"


def get_clean_data():
    try:
        res = requests.get(f"{BASE_URL}/api/standings", timeout=2).json()
        temp_df = pd.DataFrame(res)

        mapping = {
            'team': 'Team',
            'points': 'Pts', 'pts': 'Pts',
            'goals_scored': 'GS', 'gs': 'GS',
            'goals_conceded': 'GC', 'gc': 'GC',
            'goal_difference': 'GD', 'gd': 'GD'
        }
        temp_df = temp_df.rename(columns=mapping)

        # 2. Add 'GD' if it's missing (Prevents the viz error)
        if 'GD' not in temp_df.columns and 'GS' in temp_df.columns:
            temp_df['GD'] = temp_df['GS'] - temp_df['GC']

        return temp_df
    except Exception as e:
        return pd.DataFrame([
            {"Team": "Liverpool", "Pts": 63, "GS": 65, "GC": 25, "GD": 40},
            {"Team": "Man City", "Pts": 62, "GS": 63, "GC": 28, "GD": 35},
            {"Team": "Arsenal", "Pts": 61, "GS": 68, "GC": 23, "GD": 45}
        ])


if page == "Dashboard":
    st.title("📊 Premier League Pro: Season Analytics")
    df = get_clean_data()

    gs_col = 'GS' if 'GS' in df.columns else ('goals_scored' if 'goals_scored' in df.columns else 'GS')
    gc_col = 'GC' if 'GC' in df.columns else ('goals_conceded' if 'goals_conceded' in df.columns else 'GC')
    team_col = 'Team' if 'Team' in df.columns else 'team'

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏆 Current Leader", df.iloc[0][team_col])
    m2.metric("🎯 Most Clinical", f"{df.loc[df[gs_col].idxmax(), team_col]}")
    m3.metric("🛡️ Best Defense", f"{df.loc[df[gc_col].idxmin(), team_col]}")
    m4.metric("📊 Avg. Points", round(df['Pts'].mean(), 1))

    st.markdown("---")

    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.subheader("🏁 The Race for 1st Place")
        if 'GD' not in df.columns: df['GD'] = df[gs_col] - df[gc_col]
        st.bar_chart(df.set_index(team_col)[['Pts', 'GD']].head(5))
        st.caption("Comparison of Total Points vs. Goal Difference for the Top 5.")

    with col_r:
        st.subheader("🎯 Team Efficiency")
        st.scatter_chart(data=df, x=gs_col, y=gc_col, color=team_col)
        st.write("Teams at the bottom-right are the most dominant.")

    st.markdown("---")

    st.subheader("📈 Tactical Performance Breakdown")

    required_cols = ['MP', 'W', 'GD', 'Pts']
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    df['Win_Rate'] = df.apply(lambda x: (x['W'] / x['MP'] * 100) if x['MP'] > 0 else 0, axis=1)

    st.dataframe(
        df[[team_col, 'W', 'GD', 'Pts', 'Win_Rate']].sort_values('Pts', ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Win_Rate": st.column_config.ProgressColumn(
                "Win Consistency",
                format="%.0f%%",
                min_value=0,
                max_value=100
            ),
            "GD": st.column_config.NumberColumn("Goal Diff", format="%+d")
        }
    )

    st.success(
        f"**Analytics Summary:** {df.iloc[0][team_col]} is currently maintaining a {round(df['Pts'].iloc[0] / df['MP'].iloc[0], 2)} Points-Per-Game (PPG) average.")

elif page == "Squad Analytics":
    st.title("👤 Squad Depth & Market Insights")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Filter by Team")
        df = get_clean_data()
        selected_team = st.selectbox("Select Club:", df['Team'].unique())

        st.info(f"**Analytics Focus:** Showing depth charts and performance metrics for **{selected_team}**.")

    with col2:
        st.subheader(f"Projected Starting XI: {selected_team}")


        if "City" in selected_team or "Liverpool" in selected_team:
            base_rating = 88
            star_player = "Elite Forward"
        elif "Arsenal" in selected_team or "Villa" in selected_team:
            base_rating = 84
            star_player = "Key Playmaker"
        else:
            base_rating = 78
            star_player = "Lead Striker"

        squad_data = [
            {"Player": f"{selected_team} {star_player}", "Position": "FWD", "Rating": base_rating + 5, "Goals": 14},
            {"Player": f"{selected_team} Midfield", "Position": "MID", "Rating": base_rating + 2, "Goals": 4},
            {"Player": f"{selected_team} Defense", "Position": "DEF", "Rating": base_rating - 2, "Goals": 1},
            {"Player": f"{selected_team} Keeper", "Position": "GK", "Rating": base_rating, "Goals": 0}
        ]

        squad_df = pd.DataFrame(squad_data)

        st.dataframe(
            squad_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rating": st.column_config.ProgressColumn("Form Rating", min_value=0, max_value=100, format="%d pts"),
                "Goals": st.column_config.NumberColumn("Season Goals", format="%d ⚽")
            }
        )

    st.markdown("---")
    st.subheader(f"📈 Market Value Trend: {selected_team}")

    seed = len(selected_team)
    chart_data = pd.DataFrame({
        'Month': ['Aug', 'Oct', 'Dec', 'Feb', 'Mar'],
        'Value (M€)': [400 + seed, 420 + seed, 410 + seed, 450 + seed, 480 + seed]
    })
    st.line_chart(chart_data.set_index('Month'))

elif page == "League Table":
    st.title("🏟️ Premier League Standings")
    df = get_clean_data()

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("📊 Goal Difference Visualization")
    df['Goal_Diff'] = df['GS'] - df['GC']
    st.area_chart(df.set_index('Team')['Goal_Diff'])

elif page == "Live News":
    st.title("🗞️ News & Sentiment")
    if st.button("Refresh Headlines"):
        try:
            res = requests.get(f"{BASE_URL}/api/news").json()
            news_df = pd.DataFrame(res["data"])
            st.dataframe(news_df, use_container_width=True)
            st.subheader("Media Mood")
            st.bar_chart(news_df['Sentiment'].value_counts())
        except:
            st.error("Scraper Offline.")