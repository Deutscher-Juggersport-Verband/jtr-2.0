from sqlalchemy import or_

from DataDomain.Database import db
from DataDomain.Database.Model import Users
from Infrastructure.Logger import logger


class UserRepository:

    @staticmethod
    def get(userId: int) -> Users:
        return Users.query.filter_by(
            id=userId,
            is_deleted=False
        ).first()

    @staticmethod
    def getByEmail(email: str) -> Users:
        return Users.query.filter_by(
            email=email,
            is_deleted=False
        ).first()

    @staticmethod
    def exists(
            userId: int | None = None,
            escapedUsername: str | None = None,
            email: str | None = None) -> bool:

        return Users.query.filter(
            or_(
                Users.id == userId,
                Users.escaped_username == escapedUsername,
                Users.email == email,
            ),
            Users.is_deleted == False
        ).count() > 0

    @staticmethod
    def all() -> list[Users]:
        """Get user overview"""

        return Users.query.filter(Users.is_deleted == False).all()

    @staticmethod
    def usernameExists(username: str) -> bool:
        return Users.query.filter(
            Users.username == username
        ).count() > 0

    @staticmethod
    def emailExists(email: str) -> bool:
        return Users.query.filter(
            Users.email == email
        ).count() > 0

    @staticmethod
    def create(user: Users) -> int:
        try:
            db.session.add(user)
            db.session.commit()

            logger.info(
                f'UserRepository | create | User created with id {
                    user.id}')

            return user.id

        except Exception as e:
            db.session.rollback()
            logger.error(f'UserRepository | create | {e}')
            raise e

    @staticmethod
    def update(userId: int) -> None:
        try:
            db.session.commit()

            logger.info(
                f'UserRepository | update | User with id {
                    userId} updated')

        except Exception as e:
            db.session.rollback()
            logger.error(f'UserRepository | update | {e}')
            raise e

    @staticmethod
    def delete(userId: int) -> None:
        try:
            user = UserRepository.get(userId)

            user.is_deleted = True

            db.session.commit()

            logger.info(
                f'UserRepository | delete | User with id {userId} deleted')

        except Exception as e:
            db.session.rollback()
            logger.error(f'UserRepository | delete | {e}')
            raise e

    @staticmethod
    def getUserByUsername(username: str) -> Users | None:
        """Get a user by username"""

        return Users.query.filter(Users.username == username).first()

    @staticmethod
    def getUserByEmail(email: str) -> Users | None:
        """Get a user by email"""

        return Users.query.filter(Users.email == email).first()

    @staticmethod
    def getUserByUsernameOrEmail(
            username: str | None,
            email: str | None) -> Users | None:
        """Get a user by username or email"""

        return Users.query.filter(
            or_(
                Users.username == username,
                Users.email == email
            ),
            Users.is_deleted == False
        ).first()

    @staticmethod
    def getUserByPasswordResetHash(hash: str) -> Users | None:
        """Get user by password reset hash"""

        return Users.query.filter(
            Users.password_reset_hash == hash,
            Users.is_deleted == False
        ).first()
