from flask import g

from BusinessDomain.Participation.UseCase.CommandHandler import (
    CreateParticipationCommandHandler,
)
from BusinessDomain.Participation.UseCase.CommandHandler.Command import (
    CreateParticipationCommand,
)
from BusinessDomain.Tournament.Rule import DoesTournamentExistsRule
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule
from DataDomain.Model import Response


class CreateParticipationHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        teamId: int = data.get('teamId')
        tournamentId: int = data.get('tournamentId')

        if not IsCurrentUserAdminOfTeamRule.applies(teamId):
            return Response(status=403)

        if not DoesTournamentExistsRule.applies(tournamentId):
            return Response(status=404)

        try:
            CreateParticipationCommandHandler.execute(
                CreateParticipationCommand(
                    teamId=teamId,
                    tournamentId=tournamentId
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
