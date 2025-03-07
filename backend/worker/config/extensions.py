from worker.config import redis


def clearTeamHistoricPointsCache(teamId: int) -> None:

    redis.delete(f'team-historic-points-{teamId}')
