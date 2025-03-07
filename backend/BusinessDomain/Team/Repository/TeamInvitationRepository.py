
from DataDomain.Database import db
from DataDomain.Database.Model import team_invitations
from Infrastructure.Logger import logger


class TeamInvitationRepository:

    @staticmethod
    def get(hash: str) -> team_invitations:
        """Get team_invitations entry by hash"""

        return db.session.query(
            team_invitations
        ).filter(
            team_invitations.c.hash == hash
        ).first()

    @staticmethod
    def exists(userId: int, teamId: int) -> bool:
        """Check if team_invitations entry exists"""

        return db.session.query(
            db.exists().where(
                team_invitations.c.user_id == userId,
                team_invitations.c.team_id == teamId,
                team_invitations.c.is_deleted == False
            )
        ).scalar()

    @staticmethod
    def create(userId: int, teamId: int, randomHash: str) -> None:
        """Create a new team_invitations entry"""

        try:
            db.session.execute(
                team_invitations.insert().values(
                    user_id=userId,
                    team_id=teamId,
                    hash=randomHash
                )
            )
            db.session.commit()

            logger.info(f'TeamInvitationRepository | create | Created team_invitations entry for user {
                        userId} for team {teamId}')

        except Exception as e:
            db.session.rollback()
            logger.error(f'TeamInvitationRepository | create | {e}')
            raise e

    @staticmethod
    def delete(userId: int, teamId: int) -> None:
        """Set is_deleted on team_invitations entry to True"""

        try:
            db.session.execute(
                team_invitations.delete().where(
                    team_invitations.c.user_id == userId,
                    team_invitations.c.team_id == teamId
                )
            )

            logger.info(f'TeamInvitationRepository | delete | Deleted team_invitations entry for user {
                        userId} for team {teamId}')

        except Exception as e:
            db.session.rollback()
            logger.error(f'TeamInvitationRepository | delete | {e}')
            raise e

    @staticmethod
    def checkHash(userId: int, hash: str) -> bool:
        """Check if hash exists"""

        return db.session.query(
            db.exists().where(
                team_invitations.c.user_id == userId,
                team_invitations.c.hash == hash
            )
        ).scalar()

    @staticmethod
    def getTeamIdByHash(hash: str) -> int:
        """Get team by hash"""

        return db.session.query(
            team_invitations.c.team_id
        ).filter(
            team_invitations.c.hash == hash
        ).scalar()
