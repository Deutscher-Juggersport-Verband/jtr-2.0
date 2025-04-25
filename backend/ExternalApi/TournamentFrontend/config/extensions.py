from flask import request

from config import cache


def create_tournament_cache_key() -> str:

    tournamentId = request.view_args.get('tournamentId')

    return f"tournament-{tournamentId}"


def clearTournamentCache(tournamentId: int) -> None:

    cache.delete('tournament-overview')

    cache.delete(f'tournament-{tournamentId}')


def clearCompleteTournamentCache() -> None:

    tournamentKeys = cache.cache._read_client.keys('tournament-*')

    [cache.delete(key.decode('utf-8')) for key in tournamentKeys]
