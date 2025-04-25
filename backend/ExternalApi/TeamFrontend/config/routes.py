from flask import Blueprint
from flask_jwt_extended import jwt_required

from config import cache, limiter
from DataDomain.Model import Response
from ExternalApi.TeamFrontend.config import create_team_cache_key
from ExternalApi.TeamFrontend.config.extensions import (
    create_team_historic_points_cache_key,
)
from ExternalApi.TeamFrontend.Handler import (
    AcceptTeamInvitationHandler,
    CreateTeamHandler,
    DeleteMembershipHandler,
    DeleteTeamHandler,
    GetHistoricTeamPointsHandler,
    GetTeamDetailsHandler,
    GetTeamOverviewHandler,
    SendTeamInvitationHandler,
    UpdateMembershipHandler,
    UpdateTeamHandler,
    UpdateTeamPictureHandler,
)
from ExternalApi.TeamFrontend.InputFilter import (
    AcceptTeamInvitationInputFilter,
    CreateTeamInputFilter,
    DeleteMembershipInputFilter,
    DeleteTeamInputFilter,
    GetHistoricTeamPointsInputFilter,
    GetTeamDetailsInputFilter,
    SendTeamInvitationInputFilter,
    UpdateMembershipInputFilter,
    UpdateTeamInputFilter,
    UpdateTeamPictureInputFilter,
)

team_frontend = Blueprint('team-frontend', __name__)


@team_frontend.route('/get-team-details/<escapedName>',
                     methods=['GET'], endpoint='get-team-details')
@cache.cached(key_prefix=create_team_cache_key)
@GetTeamDetailsInputFilter.validate()
def getTeamDetails(escapedName) -> Response:
    return GetTeamDetailsHandler.handle()


@team_frontend.route('/get-team-overview',
                     methods=['GET'], endpoint='get-team-overview')
@cache.cached(key_prefix='team-overview')
def getTeamOverview() -> Response:
    return GetTeamOverviewHandler.handle()


@team_frontend.route('/get-historic-team-points/<teamId>',
                     methods=['GET'], endpoint='get-historic-team-points')
@cache.cached(key_prefix=create_team_historic_points_cache_key)
@GetHistoricTeamPointsInputFilter.validate()
def getHistoricTeamPoints(teamId) -> Response:
    return GetHistoricTeamPointsHandler.handle()


@team_frontend.route('/update-membership',
                     methods=['PUT'], endpoint='update-membership')
@jwt_required()
@UpdateMembershipInputFilter.validate()
def updateMembership() -> Response:
    return UpdateMembershipHandler.handle()


@team_frontend.route('/update-team',
                     methods=['PUT'], endpoint='update-team')
@limiter.limit('30 per day, 10 per hour, 3 per minute')
@jwt_required()
@UpdateTeamInputFilter.validate()
def updateTeam() -> Response:
    return UpdateTeamHandler.handle()


@team_frontend.route('/update-team-picture',
                     methods=['PUT'], endpoint='update-team-picture')
@limiter.limit('30 per day, 10 per hour, 3 per minute')
@jwt_required()
@UpdateTeamPictureInputFilter.validate()
def updateTeamPicture() -> Response:
    return UpdateTeamPictureHandler.handle()


@team_frontend.route('/create-team',
                     methods=['POST'], endpoint='create-team')
@limiter.limit('15 per day, 5 per hour, 2 per minute')
@jwt_required()
@CreateTeamInputFilter.validate()
def createTeam() -> Response:
    return CreateTeamHandler.handle()


@team_frontend.route('/send-team-invitation',
                     methods=['POST'], endpoint='send-team-invitation')
@limiter.limit('50 per day, 10 per hour, 2 per minute')
@jwt_required()
@SendTeamInvitationInputFilter.validate()
def sendTeamInvitation() -> Response:
    return SendTeamInvitationHandler.handle()


@team_frontend.route('/accept-team-invitation/<hash>',
                     methods=['POST'], endpoint='accept-team-invitation')
@limiter.limit('50 per day, 10 per hour, 2 per minute')
@jwt_required()
@AcceptTeamInvitationInputFilter.validate()
def acceptTeamInvitation(hash) -> Response:
    return AcceptTeamInvitationHandler.handle()


@team_frontend.route('/delete-membership',
                     methods=['DELETE'],
                     endpoint='delete-membership')
@jwt_required()
@DeleteMembershipInputFilter.validate()
async def deleteMembership() -> Response:
    return await DeleteMembershipHandler.handle()


@team_frontend.route('/delete-team',
                     methods=['DELETE'],
                     endpoint='delete-team')
@jwt_required()
@DeleteTeamInputFilter.validate()
async def deleteTeam() -> Response:
    return await DeleteTeamHandler.handle()
