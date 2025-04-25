from flask import g

from BusinessDomain.Team.Rule import DoesTeamExistsRule
from BusinessDomain.Team.UseCase.QueryHandler import GetTeamDetailsQueryHandler
from BusinessDomain.Team.UseCase.QueryHandler.Query import GetTeamDetailsQuery
from DataDomain.Model import Response


class GetTeamDetailsHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        escapedName: str = data.get('escapedName')

        if not DoesTeamExistsRule.applies(escapedName=escapedName):
            return Response(
                response='Team does not exist',
                status=404,
            )

        team = GetTeamDetailsQueryHandler().execute(
            GetTeamDetailsQuery(escapedName=escapedName))

        return Response(
            response=team,
            status=200,
        )
