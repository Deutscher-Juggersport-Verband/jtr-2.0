from BusinessDomain.Team.Repository import TeamRepository
from BusinessDomain.User.UseCase.QueryHandler.Query import GetTeamsWhereUserIsAdminQuery
from BusinessDomain.User.UseCase.QueryHandler.Result.GetTeamsWhereUserIsAdminResult import (
    GetTeamsWhereUserIsAdminResult, )


class GetTeamsWhereUserIsAdminQueryHandler:

    @staticmethod
    def execute(
            query: GetTeamsWhereUserIsAdminQuery) -> list[GetTeamsWhereUserIsAdminResult]:

        teams = TeamRepository.teamsOfAdmin(query.userId)

        return [GetTeamsWhereUserIsAdminResult(
            id=team.id,
            name=team.name,
            logo=team.logo,
        ) for team in teams]
