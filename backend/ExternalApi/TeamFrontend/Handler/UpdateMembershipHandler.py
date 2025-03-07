from flask import g

from BusinessDomain.Membership.UseCase.CommandHandler import (
    UpdateMembershipCommandHandler,
)
from BusinessDomain.Membership.UseCase.CommandHandler.Command import (
    UpdateMembershipCommand,
)
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule, IsUserPartOfTeamRule
from DataDomain.Model import Response


class UpdateMembershipHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        teamId: int = data.get('teamId')
        userId: int = data.get('userId')
        userRole: str = data.get('userRole')

        if not IsUserPartOfTeamRule.applies(userId=userId, teamId=teamId):
            return Response(status=404)

        if not IsCurrentUserAdminOfTeamRule.applies(teamId=teamId):
            return Response(status=403)

        try:
            UpdateMembershipCommandHandler.execute(
                UpdateMembershipCommand(
                    userId=userId,
                    teamId=teamId,
                    userRole=userRole
                )
            )

        except Exception:
            return Response(status=500)

        return Response(
            status=200
        )
