from flask import g

from BusinessDomain.Tournament.Rule import DoesTournamentExistsRule
from BusinessDomain.Tournament.UseCase.QueryHandler import (
    GetTournamentDetailsQueryHandler,
)
from BusinessDomain.Tournament.UseCase.QueryHandler.Query import GetTournamentDetailsQuery
from DataDomain.Model import Response


class GetTournamentDetailsHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        tournamentId = data.get('tournamentId')

        if not DoesTournamentExistsRule.applies(tournamentId):
            return Response(status=404, response='Tournament not found')

        tournament = GetTournamentDetailsQueryHandler.execute(
            GetTournamentDetailsQuery(
                tournamentId=tournamentId
            )
        )

        return Response(
            response=tournament,
            status=200,
        )
