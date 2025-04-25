from flask import g
from flask_jwt_extended import get_jwt_identity

from BusinessDomain.User.Rule.DoesUserExistsRule import DoesUserExistsRule
from BusinessDomain.User.UseCase.QueryHandler import GetUserDetailsQueryHandler
from BusinessDomain.User.UseCase.QueryHandler.Query import GetUserDetailsQuery
from DataDomain.Model import Response


class GetUserDetailsHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        escapedUsername: str | None = data.get('escapedUsername')

        if escapedUsername is None and get_jwt_identity() is None:
            return Response(
                status=400,
                response='Username or session is required')

        if escapedUsername is not None and not DoesUserExistsRule.applies(
                escapedUsername=escapedUsername):
            return Response(
                status=404,
                response='User not found'
            )

        user = GetUserDetailsQueryHandler.execute(
            GetUserDetailsQuery(
                escapedUsername=escapedUsername
            )
        )

        return Response(
            response=user,
            status=200,
        )
