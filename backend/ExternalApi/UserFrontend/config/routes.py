from flask import Blueprint
from flask_jwt_extended import jwt_required

from config import cache, limiter, jwt_guest_required
from DataDomain.Model import Response
from ExternalApi.UserFrontend.config.extensions import create_user_cache_key
from ExternalApi.UserFrontend.Handler import (
    AuthenticateUserHandler,
    CreateNewPasswordHandler,
    CreatePasswordResetHandler,
    CreateUserHandler,
    DeleteUserHandler,
    GetAdminOfTeamsHandler,
    GetUserDetailsHandler,
    GetUserOverviewHandler,
    IsAdminOfOrganizerHandler,
    IsAdminOfTeamHandler,
    IsMemberOfTeamHandler,
    UpdateUserHandler,
    UpdateUserLanguageHandler,
    UpdateUserPictureHandler,
)
from ExternalApi.UserFrontend.InputFilter import (
    AuthenticateUserInputFilter,
    CreateNewPasswordInputFilter,
    CreatePasswordResetInputFilter,
    CreateUserInputFilter,
    GetUserDetailsInputFilter,
    IsAdminOfOrganizerInputFilter,
    IsAdminOfTeamInputFilter,
    IsMemberOfTeamInputFilter,
    UpdateUserInputFilter,
    UpdateUserLanguageInputFilter,
    UpdateUserPictureInputFilter,
)

user_frontend = Blueprint('user-frontend', __name__)


@user_frontend.route('/get-user-details',
                     methods=['GET'], endpoint='get-user-details')
@user_frontend.route('/get-user-details/<escapedUsername>',
                     methods=['GET'], endpoint='get-user-details')
@cache.cached(key_prefix=create_user_cache_key)
@jwt_required(optional=True)
@GetUserDetailsInputFilter.validate()
def getUserDetails(escapedUsername=None) -> Response:
    return GetUserDetailsHandler.handle()


@user_frontend.route('/get-user-overview',
                     methods=['GET'], endpoint='get-user-overview')
@cache.cached(key_prefix='user-overview')
def getUserOverview() -> Response:
    return GetUserOverviewHandler.handle()


@user_frontend.route('/get-admin-teams',
                     methods=['GET'], endpoint='get-admin-teams')
@jwt_required()
def getAdminOfTeams() -> Response:
    return GetAdminOfTeamsHandler.handle()


@user_frontend.route('/is-admin-of-team/<escapedName>',
                     methods=['GET'], endpoint='is-admin-of-team')
@jwt_required()
@IsAdminOfTeamInputFilter.validate()
def isAdminOfTeam(escapedName) -> Response:
    return IsAdminOfTeamHandler.handle()


@user_frontend.route('/is-admin-of-organizer/<tournamentId>',
                     methods=['GET'], endpoint='is-admin-of-organizer')
@jwt_required()
@IsAdminOfOrganizerInputFilter.validate()
def isAdminOfOrganizer(tournamentId) -> Response:
    return IsAdminOfOrganizerHandler.handle()


@user_frontend.route('/is-member-of-team/<escapedName>',
                     methods=['GET'], endpoint='is-member-of-team')
@jwt_required()
@IsMemberOfTeamInputFilter.validate()
def isMemberOfTeam(escapedName) -> Response:
    return IsMemberOfTeamHandler.handle()


@user_frontend.route('/update-user',
                     methods=['PUT'], endpoint='update-user')
@limiter.limit('30 per day, 10 per hour, 3 per minute')
@jwt_required()
@UpdateUserInputFilter.validate()
def updateUser() -> Response:
    return UpdateUserHandler.handle()


@user_frontend.route('/update-user-picture',
                     methods=['PUT'], endpoint='update-user-picture')
@limiter.limit('30 per day, 10 per hour, 3 per minute')
@jwt_required()
@UpdateUserPictureInputFilter.validate()
def updateUserPicture() -> Response:
    return UpdateUserPictureHandler.handle()


@user_frontend.route('/update-user-language',
                     methods=['PUT'],
                     endpoint='update-user-language')
@limiter.limit('50 per day, 10 per hour, 4 per minute')
@jwt_required()
@UpdateUserLanguageInputFilter.validate()
def updateUserLanguage() -> Response:
    return UpdateUserLanguageHandler.handle()


@user_frontend.route('/authenticate-user', methods=['POST'], endpoint='authenticate-user')
@limiter.limit('60 per day, 20 per hour, 5 per minute')
@jwt_guest_required()
@AuthenticateUserInputFilter.validate()
def authenticateUser() -> Response:
    return AuthenticateUserHandler.handle()


@user_frontend.route('/create-user', methods=['POST'], endpoint='create-user')
@limiter.limit('15 per day, 7 per hour, 2 per minute')
@jwt_guest_required()
@CreateUserInputFilter.validate()
def createUser() -> Response:
    return CreateUserHandler.handle()


@user_frontend.route('/create-password-reset',
                     methods=['POST'],
                     endpoint='create-password-reset')
@limiter.limit('10 per day, 7 per hour, 2 per minute')
@jwt_guest_required()
@CreatePasswordResetInputFilter.validate()
def createPasswordReset() -> Response:
    return CreatePasswordResetHandler.handle()


@user_frontend.route('/create-new-password',
                     methods=['PUT'],
                     endpoint='create-new-password')
@limiter.limit('30 per day, 10 per hour, 2 per minute')
@jwt_guest_required()
@CreateNewPasswordInputFilter.validate()
def createNewPassword() -> Response:
    return CreateNewPasswordHandler.handle()


@user_frontend.route('/delete-user',
                     methods=['DELETE'],
                     endpoint='delete-user')
@limiter.limit('30 per day, 10 per hour, 2 per minute')
@jwt_required()
def deleteUser() -> Response:
    return DeleteUserHandler.handle()
