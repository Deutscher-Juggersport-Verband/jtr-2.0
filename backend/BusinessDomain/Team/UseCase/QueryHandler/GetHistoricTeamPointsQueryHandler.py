from BusinessDomain.Team.UseCase.QueryHandler.Query import GetHistoricTeamPointsQuery
from BusinessDomain.Team.UseCase.QueryHandler.Result import GetHistoricTeamPointsResult
from DataDomain.Database.Model import HistoricTeamPoints


class GetHistoricTeamPointsQueryHandler:

    @staticmethod
    def execute(query: GetHistoricTeamPointsQuery) -> list[GetHistoricTeamPointsResult]:

        historicPoints = HistoricTeamPoints.query.filter_by(
            team_id=query.teamId
        ).all()

        return [
            GetHistoricTeamPointsResult(
                points=historicPoint.points,
                date=historicPoint.date) for historicPoint in historicPoints]
