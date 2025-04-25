from flask import g

from BusinessDomain.User.UseCase.QueryHandler import IsAdminOfOrganizerQueryHandler
from BusinessDomain.User.UseCase.QueryHandler.Query import IsAdminOfOrganizerQuery
from DataDomain.Model import Response


class IsAdminOfOrganizerHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        isAdmin = IsAdminOfOrganizerQueryHandler.execute(
            IsAdminOfOrganizerQuery(
                tournamentId=data.get('tournamentId'),
            )
        )

        return Response(
            response=isAdmin,
            status=200,
        )
