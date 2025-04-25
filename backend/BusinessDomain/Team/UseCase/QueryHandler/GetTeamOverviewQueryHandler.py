from BusinessDomain.Team.Repository import TeamRepository
from BusinessDomain.Team.UseCase.QueryHandler.Result import TeamOverviewQueryResult


class GetTeamOverviewQueryHandler:

    @staticmethod
    def execute() -> list[TeamOverviewQueryResult]:

        teams = TeamRepository.all()

        if not teams:
            return []

        return [TeamOverviewQueryResult(
                id=team.id,
                name=team.name,
                escapedName=team.escaped_name,
                logoUrl=team.logo_url,
                points=team.points,
                placement=team.placement,
                city=team.city,
                ) for team in teams]
