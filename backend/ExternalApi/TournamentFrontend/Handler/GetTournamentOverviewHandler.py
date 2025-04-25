from BusinessDomain.Tournament.UseCase.QueryHandler import (
    GetTournamentOverviewQueryHandler,
)
from DataDomain.Model import Response


class GetTournamentOverviewHandler:

    @staticmethod
    def handle() -> Response:

        tournaments = GetTournamentOverviewQueryHandler.execute()

        return Response(
            response=tournaments,
            status=200,
        )
