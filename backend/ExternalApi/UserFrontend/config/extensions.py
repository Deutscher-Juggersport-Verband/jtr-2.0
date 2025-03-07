from flask import request

from BusinessDomain.User.Repository import UserRepository
from config import cache


def create_user_cache_key() -> str | None:

    escapedUsername = request.view_args.get('escapedUsername')

    user = UserRepository.getUserByUsername(escapedUsername)

    if user is None:
        return None

    return f"user-{user.id}"


def clearUserCache(userId: int) -> None:

    cache.delete('user-overview')

    cache.delete(f'user-{userId}')


def clearCompleteUserCache() -> None:

    userKeys = cache.cache._read_client.keys('user-*')

    [cache.delete(key.decode('utf-8')) for key in userKeys]
