from flask import g

from BusinessDomain.Participation.Rule import (
    DoesParticipationExistsRule,
    IsParticipationDeletedRule,
)
from BusinessDomain.Participation.UseCase.CommandHandler import (
    DeleteParticipationCommandHandler,
)
from BusinessDomain.Participation.UseCase.CommandHandler.Command import (
    DeleteParticipationCommand,
)
from BusinessDomain.User.Rule import (
    IsCurrentUserAdminOfOrganizingTeamRule,
    IsCurrentUserAdminOfTeamRule,
)
from DataDomain.Model import Response


class DeleteParticipationHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        teamId: int = data.get('teamId')
        tournamentId: int = data.get('tournamentId')

        if (not IsCurrentUserAdminOfTeamRule.applies(teamId)
                and not IsCurrentUserAdminOfOrganizingTeamRule.applies(tournamentId)):
            return Response(status=403)

        if not DoesParticipationExistsRule.applies(
                tournamentId=tournamentId, teamId=teamId):
            return Response(status=404)

        if IsParticipationDeletedRule.applies(tournamentId=tournamentId, teamId=teamId):
            return Response(status=400)

        try:
            DeleteParticipationCommandHandler.execute(
                DeleteParticipationCommand(
                    teamId=teamId,
                    tournamentId=tournamentId
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
