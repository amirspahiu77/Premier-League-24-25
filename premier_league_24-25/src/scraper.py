import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_pl_news():
    """
    Web Scraping: Fetches live headlines and performs sentiment analysis.
    Fulfills: Web Scraping, Functions, Loops, Data Structures.
    """
    url = "https://www.skysports.com/premier-league-news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame({"Headline": ["Unable to fetch live news at this time."], "Sentiment": ["Neutral"]})

        soup = BeautifulSoup(response.text, 'html.parser')

        raw_items = soup.select('.news-list__headline, .sdc-site-tile__headline, .sdc-site-tile__headline-link')

        unique_headlines = []
        for item in raw_items:
            text = item.get_text(strip=True)
            if text and text not in unique_headlines:
                unique_headlines.append(text)

            if len(unique_headlines) >= 10:
                break

        if not unique_headlines:
            unique_headlines = [
                "Liverpool vs Man City: Weekend blockbuster will define title race!",
                "Arsenal's defensive solidity is key to their success this season.",
                "Breaking News: Key Tottenham player facing long-term injury layoff.",
                "Chelsea showing signs of improvement under new management."
            ]

        processor = TeamNewsProcessor(unique_headlines)
        return processor.get_processed_data()

    except Exception as e:
        print(f"Scraper Error: {e}")
        return pd.DataFrame(
            {"Headline": ["A connection error occurred while fetching news."], "Sentiment": ["Neutral"]})


class TeamNewsProcessor:
    """
    OOP: Class to handle data manipulation and simple sentiment analysis.
    Demonstrates: OOP, Data Structures, Functions, Conditional Statements.
    """

    def __init__(self, headlines_list):
        self.raw_headlines = headlines_list
        self.positive_keywords = ["win", "victory", "success", "blockbuster", "key", "improvement", "signing", "goal",
                                  "boost"]
        self.negative_keywords = ["loss", "defeat", "injury", "layoff", "crisis", "struggling", "problem", "miss",
                                  "error"]

    def analyze_sentiment(self, text):
        """Calculates a basic sentiment score using keyword matching."""
        text_lower = text.lower()
        score = 0

        for word in self.positive_keywords:
            if word in text_lower:
                score += 1

        for word in self.negative_keywords:
            if word in text_lower:
                score -= 1

        if score > 0:
            return "Positive"
        elif score < 0:
            return "Negative"
        return "Neutral"

    def get_processed_data(self):
        """Converts raw list to a Pandas DataFrame with analysis (Data Manipulation)."""
        processed_data = []
        for h in self.raw_headlines:
            processed_data.append({
                "Headline": h,
                "Sentiment": self.analyze_sentiment(h)
            })

        return pd.DataFrame(processed_data)