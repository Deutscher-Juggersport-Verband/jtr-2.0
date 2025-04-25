from BusinessDomain.Tournament.Repository import TournamentRepository
from BusinessDomain.Tournament.UseCase.QueryHandler.Result import TournamentOverviewResult


class GetPastTournamentOverviewQueryHandler:

    @staticmethod
    def execute() -> list[TournamentOverviewResult]:

        tournaments = TournamentRepository.all()

        if not tournaments:
            return []

        return [TournamentOverviewResult(
            id=tournament.id,
            name=tournament.name,
            organizerLogoUrl=tournament.logo_url,
            startDate=tournament.start_date,
            endDate=tournament.end_date,
            totalTeams=tournament.possible_space,
            registeredTeams=tournament.registered_teams,
            location=tournament.location,
        ) for tournament in tournaments]
