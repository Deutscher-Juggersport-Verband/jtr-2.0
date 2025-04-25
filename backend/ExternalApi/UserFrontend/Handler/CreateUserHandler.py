from flask import g

from BusinessDomain.User.Rule import DoesEmailExistsRule, DoesUsernameExistsRule
from BusinessDomain.User.UseCase.CommandHandler import CreateUserCommandHandler
from BusinessDomain.User.UseCase.CommandHandler.Command import CreateUserCommand
from config import cache
from DataDomain.Model import Response


class CreateUserHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        username = data.get('username')
        email = data.get('email')

        if DoesUsernameExistsRule.applies(username):
            return Response(
                status=400,
                response='Username already exists'
            )

        if DoesEmailExistsRule.applies(email):
            return Response(
                status=400,
                response='Email already exists'
            )

        try:
            accessToken = CreateUserCommandHandler.execute(
                CreateUserCommand(
                    username=username,
                    email=email,
                    password=data.get('password'),
                    name=data.get('name'),
                    city=data.get('city'),
                    birthdate=data.get('birthdate'),
                    language=data.get('language'),
                    isNameVisible=data.get('isNameVisible'),
                    isCityVisible=data.get('isCityVisible'),
                    isBirthdateVisible=data.get('isBirthdateVisible')
                )
            )

            cache.delete('user-overview')

        except Exception:
            return Response(status=500)

        return Response(
            response={
                'token': accessToken,
            },
            status=200
        )
