from flask import g

from BusinessDomain.User.UseCase.QueryHandler import IsAdminOfTeamQueryHandler
from BusinessDomain.User.UseCase.QueryHandler.Query import IsAdminOfTeamQuery
from DataDomain.Model import Response


class IsAdminOfTeamHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        isAdmin = IsAdminOfTeamQueryHandler.execute(
            IsAdminOfTeamQuery(
                escapedName=data.get('escapedName')
            )
        )

        return Response(
            response=isAdmin,
            status=200,
        )
