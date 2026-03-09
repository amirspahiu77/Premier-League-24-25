import pandas as pd


class Team:
    """
    Object-Oriented Programming (OOP):
    Encapsulates all logic and data for a single Premier League club.
    """

    def __init__(self, team, points, goals_scored, goals_conceded, wins, draws, losses):
        self.name = team
        self.pts = points
        self.gs = goals_scored
        self.gc = goals_conceded
        self.w = wins
        self.d = draws
        self.l = losses

        self.mp = wins + draws + losses
        self.gd = self.gs - self.gc

    def win_rate(self) -> float:
        """Data Manipulation: Calculating custom percentages."""
        if self.mp == 0: return 0.0
        return round((self.w / self.mp) * 100, 1)

    def points_per_game(self) -> float:
        if self.mp == 0: return 0.0
        return round(self.pts / self.mp, 2)

    def get_status_tag(self) -> str:
        """Conditional Statements: Categorizing team performance."""
        if self.pts >= 60:
            return "Title Contender"
        elif self.pts >= 45:
            return "European Spot"
        elif self.pts >= 30:
            return "Mid Table"
        else:
            return "Relegation Battle"


class LeagueProcessor:
    """
    Data Structure: Manages a collection of Team objects.
    This fulfills the requirement for advanced data manipulation.
    """

    def __init__(self, raw_data_list):
        self.teams = [Team(**data) for data in raw_data_list]

    def get_dataframe(self):
        """
        Converts our custom objects into a Pandas DataFrame
        for visualization in Streamlit.
        """
        processed_data = []
        for t in self.teams:
            processed_data.append({
                "Team": t.name,
                "MP": t.mp,
                "W": t.w,
                "D": t.d,
                "L": t.l,
                "GD": t.gd,
                "Pts": t.pts,
                "Win %": t.win_rate(),
                "PPG": t.points_per_game(),
                "Status": t.get_status_tag()
            })

        df = pd.DataFrame(processed_data)
        return df.sort_values(by=["Pts", "GD"], ascending=False).reset_index(drop=True)

    def compare_teams(self, name_a, name_b):
        """
        Functionality: Logic to compare two specific objects.
        """
        team_a = next((t for t in self.teams if t.name == name_a), None)
        team_b = next((t for t in self.teams if t.name == name_b), None)

        if not team_a or not team_b:
            return "Teams not found."

        winner = team_a.name if team_a.pts > team_b.pts else team_b.name
        return {
            "leader": winner,
            "gap": abs(team_a.pts - team_b.pts),
            "attack_strength": team_a.gs if team_a.gs > team_b.gs else team_b.gs
        }