from typing import List

from sqlalchemy import String, cast, func, or_
from sqlalchemy.orm import aliased

from BusinessDomain.Team.Model import (
    OrganizedTournamentsModel,
    PastTournamentsModel,
    TeamDetailsModel,
    TeamOverviewModelElement,
)
from DataDomain.Database import db
from DataDomain.Database.Enum import UserRoleTypesEnum
from DataDomain.Database.Model import (
    Teams,
    Tournaments,
    Users,
    is_part_of,
    participates_in,
)
from Infrastructure.Logger import logger


class TeamRepository:

    @staticmethod
    def exists(teamId: int | None = None, escapedName: str | None = None) -> bool:

        return Teams.query.filter(
            or_(
                Teams.id == teamId,
                Teams.escaped_name == escapedName
            ),
            Teams.is_deleted == False
        ).count() > 0

    @staticmethod
    def all() -> List[TeamOverviewModelElement]:
        """Get team overview"""

        team_alias = aliased(Teams)
        subquery = db.session.query(
            team_alias.id,
            team_alias.points,
            func.rank().over(order_by=team_alias.points.desc()).label('rank')
        ).subquery()

        return db.session.query(
            Teams.id,
            Teams.name,
            Teams.escaped_name,
            Teams.logo_url,
            Teams.points,
            Teams.city,
            subquery.c.rank.label('placement')
        ).join(
            subquery, Teams.id == subquery.c.id
        ).filter(
            Teams.is_deleted == False
        ).order_by(
            Teams.points.desc()
        ).all()

    @staticmethod
    def getTeamDetailsById(teamId: int) -> TeamDetailsModel | None:
        """Get team details by id"""

        return db.session.query(
            Teams.id,
            Teams.name,
            Teams.escaped_name,
            Teams.logo_url,
            Teams.points,
            Teams.city,
            Teams.is_mix_team,
            Teams.created_at,
            Teams.training_time,
            Teams.training_time_updated_at,
            Teams.contacts,
            Teams.about_us,
            func.max(participates_in.c.created_at).label(
                'last_participated_tournament'),
            func.max(Tournaments.created_at).label('last_organized_tournament')
        ).outerjoin(
            participates_in, participates_in.c.team_id == Teams.id
        ).outerjoin(
            Tournaments, Tournaments.organizer_id == Teams.id
        ).filter(
            Teams.id == teamId,
            Teams.is_deleted == False
        ).group_by(
            Teams.id
        ).first()

    @staticmethod
    def getTeamMembers(teamId: int) -> List:
        """Get team members by team id"""

        return db.session.query(
            Users.id,
            Users.name,
            cast(is_part_of.c.user_role, String).label('role'),
            Users.picture_url.label('pictureUrl')
        ).join(
            is_part_of, is_part_of.c.user_id == Users.id
        ).filter(
            is_part_of.c.team_id == teamId,
            is_part_of.c.is_deleted == False
        ).all()

    @staticmethod
    def getPastTournaments(teamId: int) -> List[PastTournamentsModel]:
        """Get past tournaments by team id"""

        return db.session.query(
            Tournaments.id,
            Tournaments.name,
            Tournaments.end_date,
            participates_in.c.placement
        ).join(
            participates_in, participates_in.c.tournament_id == Tournaments.id
        ).filter(
            participates_in.c.team_id == teamId,
            participates_in.c.is_deleted == False
        ).order_by(
            Tournaments.created_at.desc()
        ).all()

    @staticmethod
    def getOrganizedTournaments(teamId: int) -> List[OrganizedTournamentsModel]:
        """Get organized tournaments by team id"""

        return db.session.query(
            Tournaments.id,
            Tournaments.name,
            Tournaments.end_date
        ).filter(
            Tournaments.organizer_id == teamId,
            Tournaments.is_deleted == False
        ).order_by(
            Tournaments.created_at.desc()
        ).all()

    @staticmethod
    def getTeamById(teamId: int) -> Teams | None:
        """Get team by id"""

        return db.session.query(
            Teams
        ).filter(
            Teams.id == teamId,
            Teams.is_deleted == False
        ).first()

    @staticmethod
    def getTeamIdByEscapedName(escapedName: str) -> int | None:
        """Get team id by escaped name"""

        team = db.session.query(
            Teams.id
        ).filter(
            Teams.escaped_name == escapedName,
            Teams.is_deleted == False
        ).first()

        return team.id if team else None

    @staticmethod
    def teamsOfUser(userId: int) -> List[Teams]:
        """Get all teams of a user"""

        return db.session.query(
            Teams
        ).join(
            is_part_of, is_part_of.c.team_id == Teams.id
        ).filter(
            is_part_of.c.user_id == userId,
            is_part_of.c.is_deleted == False
        ).all()

    @staticmethod
    def teamsOfAdmin(userId: int) -> List[Teams]:
        """Get all teams where the user is an admin"""

        return db.session.query(
            Teams
        ).join(
            is_part_of, is_part_of.c.team_id == Teams.id
        ).filter(
            is_part_of.c.user_id == userId,
            is_part_of.c.is_deleted == False,
            is_part_of.c.user_role.in_(
                [UserRoleTypesEnum.ADMIN.value, UserRoleTypesEnum.MODERATOR.value])
        ).all()

    @staticmethod
    def get(teamId: int) -> Teams | None:
        """Get team by id"""

        return Teams.query.get(teamId)

    @staticmethod
    def create(team: Teams) -> int:
        """Create a new team entry"""

        try:
            db.session.add(team)
            db.session.commit()

            return team.id

        except Exception as e:
            db.session.rollback()
            logger.error(f'TeamRepository | create |  {e}')
            raise e

    @staticmethod
    def update() -> None:
        """Update team entry"""

        try:
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(f'TeamRepository | update | {e}')
            raise e

    @staticmethod
    def delete(teamId: int) -> None:
        """Set is_deleted on team entry to True"""

        try:
            db.session.query(
                participates_in
            ).filter(
                participates_in.c.team_id == teamId,
                participates_in.c.tournament_id.in_(
                    db.session.query(Tournaments.id).filter(
                        Tournaments.end_date > func.now())
                )
            ).update({
                'is_deleted': True
            }, synchronize_session=False)

            db.session.query(
                is_part_of
            ).filter(
                is_part_of.c.team_id == teamId
            ).update({
                'is_deleted': True
            }, synchronize_session=False)

            db.session.query(
                Tournaments
            ).filter(
                Tournaments.organizer_id == teamId,
            ).update({
                'is_deleted': True
            }, synchronize_session=False)

            db.session.query(
                Teams
            ).filter(
                Teams.id == teamId
            ).update({
                'is_deleted': True
            })
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(f'TeamRepository | delete | {e}')
            raise e
