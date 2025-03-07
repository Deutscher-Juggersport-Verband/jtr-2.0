from flask import g

from BusinessDomain.Team.UseCase.CommandHandler import SendTeamInvitationCommandHandler
from BusinessDomain.Team.UseCase.CommandHandler.Command import (
    SendMembershipInvitationCommand,
)
from BusinessDomain.User.Repository import UserRepository
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule, IsUserPartOfTeamRule
from DataDomain.Model import Response


class SendTeamInvitationHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        userId: int = data.get('userId')
        teamId: int = data.get('teamId')

        if not IsCurrentUserAdminOfTeamRule.applies(teamId):
            return Response(status=403)

        user = UserRepository.get(userId)

        if IsUserPartOfTeamRule.applies(userId=userId, teamId=teamId):
            return Response(
                response='User is already a member of team',
                status=400)

        if not user:
            return Response(
                response='User not found',
                status=400)

        if not user.email:
            return Response(
                response='User has no email saved in account',
                status=400)

        try:
            SendTeamInvitationCommandHandler.execute(
                SendMembershipInvitationCommand(
                    user=user,
                    teamId=teamId
                )
            )

        except Exception:
            return Response(status=500)

        return Response(
            status=200
        )
