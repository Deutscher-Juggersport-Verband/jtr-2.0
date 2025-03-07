from flask import g

from BusinessDomain.Membership.UseCase.CommandHandler import (
    CreateMembershipCommandHandler,
)
from BusinessDomain.Membership.UseCase.CommandHandler.Command import (
    CreateMembershipCommand,
)
from BusinessDomain.Team.Rule import IsHashValidRule
from BusinessDomain.User.Rule.tools import getJwtIdentity
from DataDomain.Model import Response


class AcceptTeamInvitationHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        hash: str = data.get('hash')
        currentUserId: int = getJwtIdentity().id

        try:
            if not IsHashValidRule.applies(currentUserId, hash):
                return Response(status=400)

            CreateMembershipCommandHandler.execute(
                CreateMembershipCommand(
                    userId=currentUserId,
                    hash=hash
                )
            )

        except Exception:
            return Response(status=500)

        return Response(
            status=200
        )
