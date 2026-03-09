from fastapi import FastAPI
from src.scraper import scrape_pl_news

app = FastAPI()

@app.get("/api/standings")
def get_standings():
    return [
        {"team": "Liverpool", "points": 63, "GS": 65, "GC": 25, "wins": 19, "draws": 6, "losses": 3},
        {"team": "Man City", "points": 62, "GS": 63, "GC": 28, "wins": 18, "draws": 8, "losses": 2},
        {"team": "Arsenal", "points": 61, "GS": 68, "GC": 23, "wins": 19, "draws": 4, "losses": 5},
        {"team": "Aston Villa", "points": 55, "GS": 59, "GC": 37, "wins": 17, "draws": 4, "losses": 7},
        {"team": "Tottenham", "points": 50, "GS": 55, "GC": 39, "wins": 15, "draws": 5, "losses": 8},
        {"team": "Chelsea", "points": 45, "GS": 50, "GC": 42, "wins": 13, "draws": 6, "losses": 9},
        {"team": "Man United", "points": 44, "GS": 45, "GC": 45, "wins": 13, "draws": 5, "losses": 10}
    ]

@app.get("/api/news")
def get_news():
    news_df = scrape_pl_news()
    return {"status": "success", "data": news_df.to_dict(orient='records')}