from flask import g

from BusinessDomain.Team.Rule import DoesTeamExistsRule
from BusinessDomain.Team.UseCase.CommandHandler import DeleteTeamCommandHandler
from BusinessDomain.Team.UseCase.CommandHandler.Command import DeleteTeamCommand
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule
from DataDomain.Model import Response
from ExternalApi.TeamFrontend.config.extensions import clearTeamCache


class DeleteTeamHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        teamId: int = data.get('teamId')

        if not DoesTeamExistsRule.applies(teamId):
            return Response(status=404)

        if not IsCurrentUserAdminOfTeamRule.applies(teamId):
            return Response(status=403)

        try:
            DeleteTeamCommandHandler.execute(
                DeleteTeamCommand(
                    teamId=teamId
                )
            )

            clearTeamCache(teamId)

        except Exception:
            return Response(status=500)

        return Response(status=200)
