from flask import g

from BusinessDomain.Tournament.Rule import DoesTournamentExistsRule
from BusinessDomain.User.Rule import DoesSubscriptionExistsRule
from BusinessDomain.User.Rule.tools import getJwtIdentity
from BusinessDomain.User.UseCase.CommandHandler import (
    DeleteTournamentSubscriptionCommandHandler,
)
from BusinessDomain.User.UseCase.CommandHandler.Command import (
    DeleteTournamentSubscriptionCommand,
)
from DataDomain.Model import Response


class DeleteTournamentSubscriptionHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        tournamentId = data.get('tournamentId')
        currentUserId = getJwtIdentity().id

        if not DoesTournamentExistsRule.applies(tournamentId):
            return Response(status=404)

        if not DoesSubscriptionExistsRule.applies(
                userId=currentUserId, tournamentId=tournamentId):
            return Response(status=404)

        try:
            DeleteTournamentSubscriptionCommandHandler.execute(
                DeleteTournamentSubscriptionCommand(
                    userId=currentUserId,
                    tournamentId=tournamentId
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
