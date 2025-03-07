from BusinessDomain.Tournament.UseCase.QueryHandler import (
    GetPastTournamentOverviewQueryHandler,
)
from DataDomain.Model import Response


class GetPastTournamentOverviewHandler:

    @staticmethod
    def handle() -> Response:

        tournaments = GetPastTournamentOverviewQueryHandler.execute()

        return Response(
            response=tournaments,
            status=200,
        )
