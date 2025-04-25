from flask import g

from BusinessDomain.Tournament.UseCase.CommandHandler import (
    CreateTournamentCommandHandler,
)
from BusinessDomain.Tournament.UseCase.CommandHandler.Command import (
    CreateTournamentCommand,
)
from BusinessDomain.User.Rule import IsCurrentUserAdminOfTeamRule
from config import cache
from DataDomain.Model import Response


class CreateTournamentHandler:

    @staticmethod
    def handle() -> Response:

        data = g.validated_data

        teamId: int = data.get('teamId')

        if not IsCurrentUserAdminOfTeamRule.applies(teamId):
            return Response(status=403)

        try:
            tournamentId = CreateTournamentCommandHandler.execute(
                CreateTournamentCommand(
                    accommodationCosts=data.get('accommodationCosts'),
                    accommodationCostsType=data.get('accommodationCostsType'),
                    accommodationLocation=data.get('accommodationLocation'),
                    accommodationType=data.get('accommodationType'),
                    additionalInformation=data.get('additionalInformation'),
                    address=data.get('address'),
                    barefootAllowed=data.get('barefootAllowed'),
                    camShoesAllowed=data.get('camShoesAllowed'),
                    cleatsShoesAllowed=data.get('cleatsShoesAllowed'),
                    contacts=data.get('contacts'),
                    costsText=data.get('costsText'),
                    deadlines=data.get('deadlines'),
                    depositCosts=data.get('depositCosts'),
                    depositCostsType=data.get('depositCostsType'),
                    endArrivalDate=data.get('endArrivalDate'),
                    endDate=data.get('endDate'),
                    foodEvening=data.get('foodEvening'),
                    foodGastro=data.get('foodGastro'),
                    foodMorning=data.get('foodMorning'),
                    foodNoon=data.get('foodNoon'),
                    guestCosts=data.get('guestCosts'),
                    guestCostsType=data.get('guestCostsType'),
                    houseRulesText=data.get('houseRulesText'),
                    houseRulesUrl=data.get('houseRulesUrl'),
                    location=data.get('location'),
                    name=data.get('name'),
                    pompfCheckText=data.get('pompfCheckText'),
                    pompfCheckUrl=data.get('pompfCheckUrl'),
                    possibleSpace=data.get('possibleSpace'),
                    registrationCosts=data.get('registrationCosts'),
                    registrationCostsType=data.get('registrationCostsType'),
                    registrationProcedureText=data.get(
                        'registrationProcedureText'),
                    registrationProcedureType=data.get(
                        'registrationProcedureType'),
                    registrationStartDate=data.get(
                        'registrationStartDate'),
                    schedule=data.get('schedule'),
                    shoesText=data.get('shoesText'),
                    startArrivalDate=data.get('startArrivalDate'),
                    startDate=data.get('startDate'),
                    studdedShoesAllowed=data.get('studdedShoesAllowed'),
                    teamId=teamId,
                    tournamentSystemText=data.get('tournamentSystemText'),
                    tournamentSystemUrl=data.get('tournamentSystemUrl'),
                )
            )

            cache.delete('tournament-overview')

        except Exception:
            return Response(status=500)

        return Response(
            response=tournamentId,
            status=200
        )
