from flask import g

from BusinessDomain.Tournament.Rule import DoesTournamentExistsRule
from BusinessDomain.User.Rule import IsCurrentUserAdminOfOrganizingTeamRule
from BusinessDomain.User.UseCase.CommandHandler import (
    CreateTournamentNotificationCommandHandler,
)
from BusinessDomain.User.UseCase.CommandHandler.Command import (
    CreateTournamentNotificationCommand,
)
from DataDomain.Model import Response


class CreateTournamentNotificationHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        tournamentId: int = data.get('tournamentId')

        if not DoesTournamentExistsRule.applies(tournamentId):
            return Response(status=404)

        if not IsCurrentUserAdminOfOrganizingTeamRule.applies(
                tournamentId):
            return Response(status=403)

        try:
            CreateTournamentNotificationCommandHandler.execute(
                CreateTournamentNotificationCommand(
                    tournamentId=tournamentId,
                    message=data.get('message')
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
