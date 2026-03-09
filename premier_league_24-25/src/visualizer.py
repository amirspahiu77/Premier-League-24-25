import pandas as pd
import plotly.express as px


def plot_standings(data: list):
    """Data Manipulation and Visualization."""
    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.bar(
        df,
        x='team',
        y='points',
        color='goals_scored',
        title="Premier League Top Standings 2024/2025",
        labels={'points': 'Total Points', 'team': 'Club', 'goals_scored': 'Goals Scored'}
    )
    return fig