import os
from datetime import date, datetime
from typing import Any

from sqlalchemy import Case, case, func, literal
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped

from BusinessDomain.Common.Enum import PicturePathEnum
from DataDomain.Database import db
from DataDomain.Database.Enum import UserLanguageTypesEnum
from DataDomain.Database.Model import BaseModel, is_part_of


class Users(BaseModel, db.Model):

    __tablename__ = 'users'

    id: int = db.Column(
        db.Integer,
        primary_key=True
    )

    username: str = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    escaped_username: str = db.Column(
        db.String(100),
        nullable=False
    )

    password_hash: str = db.Column(
        db.String(255),
        nullable=False
    )

    password_reset_hash: str = db.Column(
        db.String(255),
        nullable=True
    )

    email: str | None = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    name: str | None = db.Column(
        db.String(100),
        nullable=True
    )

    name_visibility: bool = db.Column(
        db.Boolean,
        nullable=False
    )

    birthdate: date | None = db.Column(
        db.Date,
        nullable=True
    )

    birthdate_visibility: bool = db.Column(
        db.Boolean,
        nullable=False
    )

    picture: str | None = db.Column(
        db.String(255),
        nullable=True
    )

    pronouns: str | None = db.Column(
        db.String(255),
        nullable=True
    )

    city: str | None = db.Column(
        db.String(100),
        nullable=True
    )

    city_visibility: bool = db.Column(
        db.Boolean,
        nullable=False
    )

    is_deleted: bool = db.Column(
        db.Boolean,
        nullable=False,
        server_default='0'
    )

    language: UserLanguageTypesEnum = db.Column(
        db.Enum(UserLanguageTypesEnum),
        nullable=True
    )

    created_at: datetime = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    updated_at: datetime = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    teams: Mapped[list['Teams']] = db.relationship(
        'Teams',
        secondary=is_part_of,
        back_populates='team_members'
    )

    def serialize(self) -> dict[str, Any]:
        """
        Serializes the object as a dictionary.
        """

        serialized = super().serialize()

        del serialized['passwordHash']

        return serialized

    @hybrid_property
    def picture_url(self) -> str:
        """Creates the URL for the user's profile picture."""

        if self.picture is None or self.picture == '':
            return ''

        match os.getenv('FLASK_ENV'):
            case 'development':
                return f'https://cdn.localhost/assets/{
                    PicturePathEnum.USER_PICTURES_FOLDER.value}/{
                    self.picture}'

            case 'production':
                return f'https://cdn.jugger-tourna.de/assets/{
                    PicturePathEnum.USER_PICTURES_FOLDER.value}/{
                    self.picture}'

            case _:
                return self.picture

    @picture_url.expression
    def picture_url(cls) -> Case:
        """Creates the URL for the user's profile picture."""

        return case(
            (cls.picture is None, literal(None)),
            (cls.picture == '', literal(None)),
            (literal(os.getenv('FLASK_ENV')) == 'development',
             literal(f'https://cdn.localhost/assets/{PicturePathEnum.USER_PICTURES_FOLDER.value}/') + cls.picture),
            (literal(os.getenv('FLASK_ENV')) == 'production',
             literal(
                 f'https://cdn.jugger-tourna.de/assets/{PicturePathEnum.USER_PICTURES_FOLDER.value}/') + cls.picture),
            else_=cls.picture
        )
