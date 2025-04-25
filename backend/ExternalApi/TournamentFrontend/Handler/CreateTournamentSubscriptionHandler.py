from flask import g

from BusinessDomain.Tournament.Rule import DoesTournamentExistsRule
from BusinessDomain.User.Rule.tools import getJwtIdentity
from BusinessDomain.User.UseCase.CommandHandler import (
    CreateTournamentSubscriptionCommandHandler,
)
from BusinessDomain.User.UseCase.CommandHandler.Command import (
    CreateTournamentSubscriptionCommand,
)
from DataDomain.Model import Response


class CreateTournamentSubscriptionHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        tournamentId: int = data.get('tournamentId')

        if not DoesTournamentExistsRule.applies(tournamentId):
            return Response(status=404)

        try:
            CreateTournamentSubscriptionCommandHandler.execute(
                CreateTournamentSubscriptionCommand(
                    tournamentId=tournamentId,
                    userId=getJwtIdentity().id
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
