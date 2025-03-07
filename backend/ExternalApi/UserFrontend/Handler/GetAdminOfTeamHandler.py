from BusinessDomain.User.Rule.tools import getJwtIdentity
from BusinessDomain.User.UseCase.QueryHandler import GetTeamsWhereUserIsAdminQueryHandler
from BusinessDomain.User.UseCase.QueryHandler.Query.GetTeamsWhereUserIsAdminQuery import (
    GetTeamsWhereUserIsAdminQuery,
)
from DataDomain.Model import Response


class GetAdminOfTeamsHandler:

    @staticmethod
    def handle() -> Response:

        teams = GetTeamsWhereUserIsAdminQueryHandler.execute(
            GetTeamsWhereUserIsAdminQuery(
                userId=getJwtIdentity().id
            )
        )

        return Response(
            response=teams,
            status=200,
        )
