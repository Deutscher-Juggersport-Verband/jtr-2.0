from flask import g

from BusinessDomain.Participation.UseCase.CommandHandler import CreateResultCommandHandler
from BusinessDomain.Participation.UseCase.CommandHandler.Command import (
    CreateResultCommand,
)
from BusinessDomain.Tournament.Model import ResultElement
from BusinessDomain.Tournament.Rule import DoesTournamentExistsRule
from BusinessDomain.User.Rule import IsCurrentUserAdminOfOrganizingTeamRule
from DataDomain.Model import Response
from ExternalApi.TournamentFrontend.config.extensions import clearTournamentCache


class CreateResultHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        tournamentId: int = data.get('tournamentId')

        if not DoesTournamentExistsRule.applies(tournamentId):
            return Response(status=404)

        if not IsCurrentUserAdminOfOrganizingTeamRule.applies(
                tournamentId):
            return Response(status=403)

        try:
            CreateResultCommandHandler.execute(
                CreateResultCommand(
                    tournamentId=tournamentId,
                    resultElements=[
                        ResultElement(
                            **e) for e in data.get('resultElements')]))

            clearTournamentCache(tournamentId)

        except Exception:
            return Response(status=500)

        return Response(status=200)
