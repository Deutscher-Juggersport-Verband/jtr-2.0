from flask import g

from BusinessDomain.Team.Rule import DoesTeamExistsRule
from BusinessDomain.Team.UseCase.CommandHandler import UpdateTeamCommandHandler
from BusinessDomain.Team.UseCase.CommandHandler.Command import UpdateTeamCommand
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule
from DataDomain.Model import Response
from ExternalApi.TeamFrontend.config.extensions import clearTeamCache


class UpdateTeamHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        teamId = data.get('teamId')

        if not DoesTeamExistsRule.applies(teamId):
            return Response(status=404)

        # TODO: escapedName creation and check
        # escapedName = data.get('escapedName')
        escapedName = data.get('name').lower().replace(' ', '-')

        if not IsCurrentUserAdminOfTeamRule.applies(
                teamId):
            return Response(status=403)

        try:
            UpdateTeamCommandHandler.execute(
                UpdateTeamCommand(
                    aboutUs=data.get('aboutUs'),
                    city=data.get('city'),
                    contacts=data.get('contacts'),
                    escapedName=escapedName,
                    founded=data.get('founded'),
                    isMixTeam=data.get('isMixTeam'),
                    logo=data.get('logo'),
                    name=data.get('name'),
                    teamId=teamId,
                    trainingTime=data.get('trainingTime')
                )
            )

            clearTeamCache(teamId)

        except Exception:
            return Response(status=500)

        return Response(
            status=200
        )
