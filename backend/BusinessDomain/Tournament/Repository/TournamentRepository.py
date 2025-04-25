from datetime import datetime

from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import aliased, joinedload

from BusinessDomain.Tournament.Model import TournamentOverviewModelElement
from BusinessDomain.User.Rule.tools import getJwtIdentity
from DataDomain.Database import db
from DataDomain.Database.Enum import TournamentStatusTypesEnum
from DataDomain.Database.Model import Teams, Tournaments, participates_in
from Infrastructure.Logger import logger


class TournamentRepository:
    """Repository for tournament related queries"""

    @staticmethod
    def all() -> list[TournamentOverviewModelElement]:

        currentTime = datetime.now()

        TeamParticipation = aliased(participates_in)

        return db.session.query(
            Tournaments.id,
            Tournaments.organizer_id,
            Tournaments.name,
            Tournaments.start_date,
            Tournaments.end_date,
            Teams.logo_url.label('logo_url'),
            Tournaments.possible_space,
            func.count(
                TeamParticipation.c.team_id).label('registered_teams'),
            Tournaments.location
        ).outerjoin(
            TeamParticipation,
            Tournaments.id == TeamParticipation.c.tournament_id
        ).join(
            Teams,
            Tournaments.organizer_id == Teams.id
        ).filter(
            or_(
                and_(
                    Tournaments.start_date <= currentTime,
                    Tournaments.end_date >= currentTime
                ),
                Tournaments.start_date > currentTime
            ),
            Tournaments.is_deleted == False,
            Tournaments.status == TournamentStatusTypesEnum.PUBLISHED.value
        ).group_by(
            Tournaments.id
        ).order_by(
            Tournaments.start_date
        ).all()

    @staticmethod
    def getPastTournamentOverview() -> list[TournamentOverviewModelElement]:

        currentTime = datetime.now()

        TeamParticipation = aliased(participates_in)

        return db.session.query(
            Tournaments.id,
            Tournaments.organizer_id,
            Tournaments.name,
            Tournaments.start_date,
            Tournaments.end_date,
            Teams.logo_url.label('logo_url'),
            Tournaments.possible_space,
            func.count(
                TeamParticipation.c.team_id).label('registered_teams'),
            Tournaments.location
        ).outerjoin(
            TeamParticipation,
            Tournaments.id == TeamParticipation.c.tournament_id
        ).join(
            Teams,
            Tournaments.organizer_id == Teams.id
        ).filter(
            Tournaments.end_date < currentTime,
            Tournaments.is_deleted == False
        ).group_by(
            Tournaments.id
        ).order_by(
            desc(
                Tournaments.start_date
            )
        ).all()

    @staticmethod
    def get(tournamentId: int) -> Tournaments:

        return db.session.query(
            Tournaments
        ).filter(
            Tournaments.id == tournamentId,
            Tournaments.is_deleted == False
        ).first()

    @staticmethod
    def getFull(tournamentId: int):

        return db.session.query(Tournaments).options(
            joinedload(Tournaments.teams),
            joinedload(Tournaments.organizer)
        ).filter(
            Tournaments.id == tournamentId,
            Tournaments.is_deleted == False
        ).first()

    @staticmethod
    def getByName(name: str) -> Tournaments:

        return db.session.query(
            Tournaments
        ).filter(
            Tournaments.name == name,
            Tournaments.is_deleted == False
        ).first()

    @staticmethod
    def exists(tournamentId: int) -> bool:

        return Tournaments.query.filter(
            Tournaments.id == tournamentId,
            Tournaments.is_deleted == False
        ).count() > 0

    @staticmethod
    def create(tournament: Tournaments) -> int:

        try:
            db.session.add(tournament)
            db.session.commit()

            user = getJwtIdentity()

            logger.info(
                f'TournamentRepository | Create | User {
                    user.id} created tournament {
                    tournament.id}')

            return tournament.id

        except Exception as e:
            db.session.rollback()
            logger.error(f'TournamentRepository | Create | {e}')
            raise e

    @staticmethod
    def update(tournament: Tournaments) -> None:

        try:
            db.session.commit()

            user = getJwtIdentity()

            logger.info(
                f'TournamentRepository | Update | User {
                    user.id} updated tournament {
                    tournament.id}')

        except Exception as e:
            db.session.rollback()
            logger.error(f'TournamentRepository | Update | {e}')
            raise e

    @staticmethod
    def delete(tournamentId: int) -> None:

        try:
            db.session.query(
                participates_in
            ).filter(
                participates_in.c.tournament_id == tournamentId
            ).update({
                'is_deleted': True
            }, synchronize_session=False)

            db.session.query(
                Tournaments
            ).filter(
                Tournaments.id == tournamentId
            ).update({
                'is_deleted': True
            })
            db.session.commit()

            user = getJwtIdentity()

            logger.info(
                f'TournamentRepository | Delete | User {
                    user.id} deleted tournament {tournamentId}')

        except Exception as e:
            db.session.rollback()
            logger.error(f'TournamentRepository | Delete | {e}')
            raise e

    @staticmethod
    def getOrganizingTeam(tournamentId: int) -> Teams | None:

        return db.session.query(
            Teams
        ).join(
            Tournaments,
            Tournaments.organizer_id == Teams.id
        ).filter(
            Tournaments.id == tournamentId
        ).first()
