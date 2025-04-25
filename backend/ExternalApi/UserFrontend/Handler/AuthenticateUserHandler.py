from flask import g

from BusinessDomain.User.Repository import UserRepository
from BusinessDomain.User.UseCase.CommandHandler import LoginUserCommandHandler
from BusinessDomain.User.UseCase.CommandHandler.Command import LoginUserCommand
from DataDomain.Model import Response


class AuthenticateUserHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        username: str | None = data.get('username')
        email: str | None = data.get('email')

        if username is None and email is None:
            return Response(
                response='Benutzername oder Email muss angegeben werden.',
                status=400
            )

        user = UserRepository.getUserByUsernameOrEmail(username, email)

        if user is None:
            return Response(
                response='Falsche Anmeldedaten.',
                status=401
            )

        loginUserResult = LoginUserCommandHandler.execute(
            LoginUserCommand(
                username=user.username,
                email=user.email,
                password=data.get('password')
            )
        )

        if not loginUserResult:
            return Response(
                response='Falsche Anmeldedaten.',
                status=401
            )

        if loginUserResult.token is not None:
            return Response(
                response={
                    'token': loginUserResult.token,
                    'language': user.language,
                },
                status=200,
            )

        if loginUserResult.lockType is not None:
            return Response(
                response={
                    'lockType': loginUserResult.lockType,
                    'lockedUntil': loginUserResult.lockedUntil
                },
                status=401
            )

        return Response(
            response='Falsche Anmeldedaten.',
            status=401
        )
