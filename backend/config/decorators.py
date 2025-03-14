from functools import wraps
from typing import Any, Optional, Sequence, Union

from flask import current_app
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import InvalidHeaderError, NoAuthorizationError

from DataDomain.Model import Response


def jwt_guest_required(
    optional: bool = False,
    fresh: bool = False,
    refresh: bool = False,
    locations: Optional[Union[str, Sequence, None]] = None,
    verify_type: bool = True,
    skip_revocation_check: bool = False,
) -> Any:
    """
    A decorator to ensure no valid JWT is present in the request.

    Any route decorated with this will require an invalid JWT to be present in the
    request before the endpoint can be called. If a valid JWT is present, an error
    message will be returned.

    :param optional:
        If ``True``, allow the decorated endpoint to be accessed if no JWT is present in
        the request. Defaults to ``False``.

    :param fresh:
        If ``True``, require a JWT marked with ``fresh`` to be able to access this
        endpoint. Defaults to ``False``.

    :param refresh:
        If ``True``, requires a refresh JWT to access this endpoint. If ``False``,
        requires an access JWT to access this endpoint. Defaults to ``False``.

    :param locations:
        A location or list of locations to look for the JWT in this request, for
        example ``'headers'`` or ``['headers', 'cookies']``. Defaults to ``None``
        which indicates that JWTs will be looked for in the locations defined by the
        ``JWT_TOKEN_LOCATION`` configuration option.

    :param verify_type:
        If ``True``, the token type (access or refresh) will be checked according
        to the ``refresh`` argument. If ``False``, type will not be checked and both
        access and refresh tokens will be accepted.

    :param skip_revocation_check:
        If ``True``, revocation status of the token will be *not* checked. If ``False``,
        revocation status of the token will be checked.
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request(
                    optional,
                    fresh,
                    refresh,
                    locations,
                    verify_type,
                    skip_revocation_check)
                return Response("Valid token should not be provided", 400)
            except (NoAuthorizationError, InvalidHeaderError):
                pass
            return current_app.ensure_sync(fn)(*args, **kwargs)
        return decorator
    return wrapper
