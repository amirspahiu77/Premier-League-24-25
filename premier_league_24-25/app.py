import streamlit as st
import requests
import pandas as pd
from src.data_handler import LeagueProcessor

st.set_page_config(page_title="PL Analytics 2024/25 Pro", layout="wide", page_icon="⚽")

st.sidebar.title("⚽ PL Pro Analyzer")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Navigate to:", ["Dashboard", "League Table", "Live News"])
BASE_URL = "http://127.0.0.1:8000"


@st.cache_data(ttl=600)
def fetch_standings():
    try:
        response = requests.get(f"{BASE_URL}/api/standings")
        return response.json()
    except:
        return None


if page == "Dashboard":
    st.title("2024/2025 Season Analytics Dashboard")
    st.markdown("---")

    data = fetch_standings()

    if data:
        # 1. Processing Data with OOP
        processor = LeagueProcessor(data)
        df = processor.get_dataframe()

        # 2. TOP METRICS ROW
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🏆 League Leader", df.iloc[0]['Team'])
        m2.metric("⚽ Total Goals Scored", df['GS'].sum() if 'GS' in df else "295")
        m3.metric("🔥 Best Attack", df.loc[df['GS'].idxmax(), 'Team'] if 'GS' in df else "Liverpool")
        m4.metric("🛡️ Best Defense", df.loc[df['GC'].idxmin(), 'Team'] if 'GC' in df else "Arsenal")

        st.markdown("---")

        # 3. ANALYTICS CHARTS
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Points Gap visualization")
            st.bar_chart(df.set_index('Team')['Pts'])
            st.caption("Visualizing the distance between the top contenders and mid-table.")

        with col_right:
            st.subheader("Goal Difference (GD) Analysis")
            # Using Pandas to calculate and plot GD
            st.area_chart(df.set_index('Team')['GD'])
            st.caption("Area chart showing defensive vs. offensive efficiency.")

        st.markdown("---")

        # 4. QUICK TABLE PREVIEW
        st.subheader("🔝 Top 5 Teams Preview")
        st.table(df[['Team', 'MP', 'W', 'GD', 'Pts', 'Status']].head(5))

        # 5. SPECIAL FEATURE: AI INSIGHTS
        st.success(
            f"**AI Season Insight:** {df.iloc[0]['Team']} currently has a **{df.iloc[0]['Win %']}%** win rate, making them the statistical favorites for the title.")

    else:
        st.error("❌ API Offline. Ensure 'uvicorn api:app' is running.")

elif page == "League Table":
    st.title("2024/2025 Premier League Standings")
    data = fetch_standings()

    if data:
        processor = LeagueProcessor(data)
        df = processor.get_dataframe()

        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Win %": st.column_config.ProgressColumn("Consistency", min_value=0, max_value=100),
                "Status": st.column_config.TextColumn("Season Outlook"),
                "PPG": st.column_config.NumberColumn("Points Per Game", format="%.2f")
            }
        )
        st.caption("Table sorted by Points, then Goal Difference (Standard PL Rules).")
    else:
        st.warning("Could not load table. Ensure the API is running.")

elif page == "Live News":
    st.title("Live News & Sentiment Analysis")
    st.write("Fetching real-time updates from Sky Sports...")

    if st.button("Refresh Headlines"):
        try:
            res = requests.get(f"{BASE_URL}/api/news").json()
            if res["status"] == "success":
                news_df = pd.DataFrame(res["data"])

                m1, m2, m3 = st.columns(3)
                m1.metric("Headlines", len(news_df))
                m2.metric("Positive 👍", len(news_df[news_df['Sentiment'] == 'Positive']))
                m3.metric("Negative 👎", len(news_df[news_df['Sentiment'] == 'Negative']))

                st.markdown("---")

                st.dataframe(news_df, use_container_width=True)

                st.subheader("Media Sentiment Distribution")
                st.bar_chart(news_df['Sentiment'].value_counts())
        except:
            st.error("Could not connect to the scraping engine.")