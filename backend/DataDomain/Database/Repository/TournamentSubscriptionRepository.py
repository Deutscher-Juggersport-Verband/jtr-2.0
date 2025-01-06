from typing import List

from DataDomain.Database.Model.TournamentSubscriptions import tournament_subscriptions
from DataDomain.Database.Model.Users import Users
from DataDomain.Database.db import db
from Infrastructure.Logger.Logger import logger


class TournamentSubscriptionRepository:
    """Repository for tournament_subscriptions related queries"""

    @staticmethod
    def get(userId: int, tournamentId: int) -> tournament_subscriptions:
        """Get tournament_subscriptions entry by tournamentId"""

        return db.session.query(
            tournament_subscriptions
        ).filter(
            tournament_subscriptions.c.user_id == userId,
            tournament_subscriptions.c.tournament_id == tournamentId
        ).first()

    @staticmethod
    def getRecipients(tournamentId: int) -> List[Users]:
        """Get all subscribed users entry's by tournamentId"""

        return Users.query.join(
            tournament_subscriptions,
            tournament_subscriptions.c.user_id == Users.id
        ).filter_by(
            tournament_subscriptions.c.tournamentId == tournamentId
        ).all()

    @staticmethod
    def exists(userId: int, tournamentId: int) -> bool:
        """Check if tournament_subscriptions entry exists"""

        return db.session.query(
            db.exists().where(
                tournament_subscriptions.c.user_id == userId,
                tournament_subscriptions.c.tournament_id == tournamentId
            )
        ).scalar()

    @staticmethod
    def create(userId: int, tournamentId: int) -> None:
        """Create a new tournament_subscriptions entry"""

        try:
            db.session.execute(
                tournament_subscriptions.insert().values(
                    user_id=userId,
                    tournament_id=tournamentId
                )
            )
            db.session.commit()

            logger.info(f'TournamentSubscriptionsRepository | create | Created tournament_subscriptions entry for user {
                        userId} and tournament {tournamentId}')

        except Exception as e:
            db.session.rollback()
            logger.error(f'TournamentSubscriptionsRepository | create | {e}')
            raise e

    @staticmethod
    def delete(userId: int, tournamentId: int) -> None:
        """Set is_deleted on tournament_subscriptions entry to True"""

        try:
            db.session.execute(
                tournament_subscriptions.delete().where(
                    tournament_subscriptions.c.user_id == userId,
                    tournament_subscriptions.c.tournament_id == tournamentId
                )
            )

            logger.info(f'TournamentSubscriptionsRepository | delete | Deleted tournament_subscriptions entry for user {
                        userId} and tournament {tournamentId}')

        except Exception as e:
            db.session.rollback()
            logger.error(f'TournamentSubscriptionsRepository | delete | {e}')
            raise e
