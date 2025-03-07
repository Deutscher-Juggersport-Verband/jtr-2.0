from DataDomain.Database import db
from DataDomain.Database.Model import LoginAttempts
from Infrastructure.Logger import logger


class LoginAttemptRepository:

    @staticmethod
    def exists(username: str) -> bool:
        """Check if a LoginAttempt entry exists"""

        return LoginAttempts.query.filter_by(
            username=username).first() is not None

    @staticmethod
    def update() -> None:
        """Update a LoginAttempt entry"""

        try:
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(
                f'LoginAttemptRepository | update | {e}')
            raise e

    @staticmethod
    def create(username: str) -> LoginAttempts:
        """Create a new LoginAttempt entry"""

        try:
            loginAttempt = LoginAttempts()

            loginAttempt.username = username

            db.session.add(loginAttempt)
            db.session.commit()

            logger.info(
                f'LoginAttemptRepository | create | Created new failed login attempt for user {username}')

            return loginAttempt

        except Exception as e:
            db.session.rollback()
            logger.error(f'LoginAttemptRepository | create | {e}')
            raise e

    @staticmethod
    def getByUsername(username: str) -> LoginAttempts | None:
        """Get a LoginAttempt entry by username"""

        return LoginAttempts.query.filter_by(username=username).first()
