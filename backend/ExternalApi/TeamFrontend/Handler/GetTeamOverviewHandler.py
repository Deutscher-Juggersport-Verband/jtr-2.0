from BusinessDomain.Team.UseCase.QueryHandler import GetTeamOverviewQueryHandler
from DataDomain.Model import Response


class GetTeamOverviewHandler:

    @staticmethod
    def handle() -> Response:

        team = GetTeamOverviewQueryHandler.execute()

        return Response(
            response=team,
            status=200,
        )
