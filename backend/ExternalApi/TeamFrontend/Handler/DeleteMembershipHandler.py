from flask import g

from BusinessDomain.Membership.UseCase.CommandHandler import (
    DeleteMembershipCommandHandler,
)
from BusinessDomain.Membership.UseCase.CommandHandler.Command import (
    DeleteMembershipCommand,
)
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule, IsUserPartOfTeamRule
from BusinessDomain.User.Rule.tools import getJwtIdentity
from DataDomain.Model import Response


class DeleteMembershipHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        currentUser = getJwtIdentity()

        teamId = data.get('teamId')
        userId = data.get('userId') or currentUser.id

        if not IsUserPartOfTeamRule.applies(userId, teamId):
            return Response(status=401)

        if (data.get(
                'userId') and not IsCurrentUserAdminOfTeamRule.applies(teamId)):
            return Response(status=403)

        try:
            DeleteMembershipCommandHandler.execute(
                DeleteMembershipCommand(
                    userId=userId,
                    teamId=teamId
                )
            )

        except Exception:
            return Response(status=500)

        return Response(status=200)
