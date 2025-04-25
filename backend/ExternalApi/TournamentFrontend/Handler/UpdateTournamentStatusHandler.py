from flask import g

from BusinessDomain.Tournament.UseCase.CommandHandler import (
    UpdateTournamentStatusCommandHandler,
)
from BusinessDomain.Tournament.UseCase.CommandHandler.Command import (
    UpdateTournamentStatusCommand,
)
from BusinessDomain.User.Rule import IsCurrentUserAdminOfOrganizingTeamRule
from DataDomain.Model import Response
from ExternalApi.TournamentFrontend.config.extensions import clearTournamentCache


class UpdateTournamentStatusHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        tournamentId: int = data.get('tournamentId')

        if not IsCurrentUserAdminOfOrganizingTeamRule.applies(tournamentId):
            return Response(status=403)

        try:
            UpdateTournamentStatusCommandHandler.execute(
                UpdateTournamentStatusCommand(
                    tournamentId=tournamentId,
                    status=data.get('status')
                )
            )

            clearTournamentCache(tournamentId)

        except Exception:
            return Response(status=500)

        return Response(
            status=200
        )
