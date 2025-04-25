from datetime import datetime

from sqlalchemy import func, select

from DataDomain.Database.Model import (
    HistoricTeamPoints,
    Teams,
    Tournaments,
    participates_in,
)
from worker.config import clearTeamHistoricPointsCache
from worker.db import db


class CalculateTeamScoresHandler:

    FACTORS = [0.24, 0.22, 0.20, 0.18, 0.16]
    PLACE_POINTS = [
        0, 0, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 16, 17, 17, 18,
        18, 19, 19, 20, 20, 20, 20, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22,
        22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
        23, 23, 24, 24, 24, 24, 24
    ]

    SUBQUERY = select(func.count()).filter(
        participates_in.c.tournament_id == Tournaments.id,
        participates_in.c.is_deleted == False,
        participates_in.c.has_played == True
    ).correlate(Tournaments).scalar_subquery()

    CURRENT_DATE = None

    def handle(self) -> None:
        self.CURRENT_DATE = datetime.utcnow()

        teams = db.query(Teams).all()

        for team in teams:
            tournaments = db.query(
                participates_in.c.placement,
                Tournaments.end_date,
                self.SUBQUERY.label('num_teams')
            ).join(
                Tournaments,
                participates_in.c.tournament_id == Tournaments.id,
            ).filter(
                participates_in.c.is_deleted == False,
                Tournaments.end_date <= self.CURRENT_DATE,
                participates_in.c.has_played == True,
                participates_in.c.team_id == team.id
            ).all()

            formatted_tournaments = [
                {
                    'placement': t.placement,
                    'numTeams': t.num_teams,
                    'endDate': t.end_date,
                }
                for t in tournaments
            ]

            newPointScore = self.calculateTotalScore(formatted_tournaments)

            team.points = newPointScore

            historicTeamPoints = HistoricTeamPoints()
            historicTeamPoints.team_id = team.id,
            historicTeamPoints.points = newPointScore,
            historicTeamPoints.date = self.CURRENT_DATE

            db.add(historicTeamPoints)
            db.commit()

            clearTeamHistoricPointsCache(team.id)

    def calculateBruttoTournamentPoints(self, numTeams: int, placement: int):
        """Calculates the brutto tournament points based on the tournament placement."""

        if numTeams >= len(self.PLACE_POINTS):
            raise ValueError(
                "Die Anzahl der Teams überschreitet die Punktetabelle.")

        maxPoints = self.PLACE_POINTS[numTeams]

        deltaTw = maxPoints / (numTeams - 1)

        return (numTeams - placement) * deltaTw

    def calculateTimeFactor(self, endDate):
        """Calculates the time factor based on the tournament end date."""

        monthsPassed = (self.CURRENT_DATE.year - endDate.year) * \
            12 + self.CURRENT_DATE.month - endDate.month

        return pow(0.75, monthsPassed // 6)

    def calculateRelevanceFactor(self, placement):
        """Calculates the relevance factor based on the tournament placement."""

        return self.FACTORS[placement - 1] if 1 <= placement <= 5 else 0

    def calculateTeamScore(self, placement, numTeams, endDate):
        """Calculates the total score for a team based on the tournament placement."""

        bruttoPoints = self.calculateBruttoTournamentPoints(
            numTeams, placement)
        timeFactor = self.calculateTimeFactor(endDate)

        return bruttoPoints * timeFactor

    def calculateTotalScore(self, tournaments):
        """Calculates the total score for a team based on the top 5 tournament scores."""

        scores = [self.calculateTeamScore(**tournament)
                  for tournament in tournaments]
        scores.sort(reverse=True)
        top5Scores = [score *
                      self.calculateRelevanceFactor(placement +
                                                    1) for placement, score in enumerate(scores[:5])]

        return sum(top5Scores)
