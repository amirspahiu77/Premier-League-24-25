from fastapi import FastAPI
from src.scraper import scrape_pl_news
from fastapi import FastAPI
from src.scraper import scrape_pl_news

app = FastAPI(title="Premier League Pro API")

@app.get("/api/standings")
def get_standings():
    # Full list for the Dashboard and League Table
    return [
        {"team": "Liverpool", "points": 63, "goals_scored": 65, "goals_conceded": 25, "wins": 19, "draws": 6, "losses": 3},
        {"team": "Man City", "points": 62, "goals_scored": 63, "goals_conceded": 28, "wins": 18, "draws": 8, "losses": 2},
        {"team": "Arsenal", "points": 61, "goals_scored": 68, "goals_conceded": 23, "wins": 19, "draws": 4, "losses": 5},
        {"team": "Aston Villa", "points": 55, "goals_scored": 59, "goals_conceded": 37, "wins": 17, "draws": 4, "losses": 7},
        {"team": "Tottenham", "points": 50, "goals_scored": 55, "goals_conceded": 39, "wins": 15, "draws": 5, "losses": 8},
        {"team": "Chelsea", "points": 45, "goals_scored": 50, "goals_conceded": 42, "wins": 13, "draws": 6, "losses": 9},
        {"team": "Man United", "points": 44, "goals_scored": 45, "goals_conceded": 45, "wins": 13, "draws": 5, "losses": 10}
    ]

@app.get("/api/news")
def get_news():
    news_df = scrape_pl_news()
    return {"status": "success", "data": news_df.to_dict(orient='records')}