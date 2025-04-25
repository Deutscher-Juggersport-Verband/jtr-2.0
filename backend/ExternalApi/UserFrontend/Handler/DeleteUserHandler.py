from BusinessDomain.User.Rule.tools import getJwtIdentity
from BusinessDomain.User.UseCase.CommandHandler import DeleteUserCommandHandler
from BusinessDomain.User.UseCase.CommandHandler.Command import DeleteUserCommand
from DataDomain.Model import Response


class DeleteUserHandler:

    @staticmethod
    def handle() -> Response:

        currentUser = getJwtIdentity()

        if currentUser.is_deleted:
            return Response(status=404)

        try:
            DeleteUserCommandHandler.execute(
                DeleteUserCommand(
                    userId=currentUser.id
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
