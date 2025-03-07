from flask import g
from flask_jwt_extended import get_jwt_identity

from BusinessDomain.User.UseCase.CommandHandler import UpdateUserCommandHandler
from BusinessDomain.User.UseCase.CommandHandler.Command import UpdateUserCommand
from DataDomain.Model import Response
from ExternalApi.UserFrontend.config.extensions import clearUserCache


class UpdateUserHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        try:
            accessToken = UpdateUserCommandHandler.execute(
                UpdateUserCommand(
                    birthdate=data.get('birthdate'),
                    city=data.get('city'),
                    email=data.get('email'),
                    isBirthdateVisible=data.get('isBirthdateVisible'),
                    isCityVisible=data.get('isCityVisible'),
                    isNameVisible=data.get('isNameVisible'),
                    name=data.get('name'),
                    password=data.get('password'),
                    pronouns=data.get('pronouns'),
                    username=data.get('username'),
                )
            )

            clearUserCache(get_jwt_identity())

        except Exception:
            return Response(status=500)

        return Response(
            response={
                'token': accessToken,
            },
            status=200
        )
