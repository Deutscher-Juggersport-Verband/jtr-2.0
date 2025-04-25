import json
import os
from datetime import datetime
from typing import Any

from sqlalchemy import Case, case, func, literal
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped

from BusinessDomain.Common.Enum import PicturePathEnum
from DataDomain.Database import db
from DataDomain.Database.Model import BaseModel, is_part_of, participates_in


class Teams(BaseModel, db.Model):

    __tablename__ = 'teams'

    id: int = db.Column(
        db.Integer,
        primary_key=True
    )

    name: str = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    escaped_name: str = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    logo: str | None = db.Column(
        db.String(255),
        nullable=True
    )

    founded: datetime | None = db.Column(
        db.DateTime,
        nullable=True
    )

    points: float = db.Column(
        db.Float,
        server_default='0'
    )

    city: str | None = db.Column(
        db.String(100),
        nullable=True
    )

    training_time: str | None = db.Column(
        db.String(100),
        nullable=True
    )

    training_time_updated_at: datetime | None = db.Column(
        db.DateTime,
        nullable=True
    )

    about_us: str | None = db.Column(
        db.String(100),
        nullable=True,
    )

    contacts: str = db.Column(
        db.Text,
        nullable=False,
        default='[]',
        doc='["string"]'
    )

    is_mix_team: bool | None = db.Column(
        db.Boolean,
        nullable=True
    )

    is_deleted: bool = db.Column(
        db.Boolean,
        nullable=False,
        server_default='0'
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

    team_members: Mapped[list['Users']] = db. relationship(
        'Users',
        secondary=is_part_of,
        back_populates='teams'
    )

    tournaments: Mapped[list['Tournaments']] = db.relationship(
        'Tournaments',
        secondary=participates_in,
        back_populates='teams'
    )

    organized_tournaments: Mapped[list['Tournaments']] = db.relationship(
        'Tournaments',
        back_populates='organizer'
    )

    historic_points: Mapped[list['HistoricTeamPoints']] = db.relationship(
        'HistoricTeamPoints',
        back_populates='team'
    )

    def serialize(self) -> dict[str, Any]:
        """
        Serializes the object as a dictionary.
        """

        serialized = super().serialize()

        serialized['contacts'] = self.getContacts

        if serialized.get('trainingTimeUpdatedAt'):
            serialized['trainingTimeUpdatedAt'] = serialized.pop(
                'trainingTimeUpdatedAt').isoformat()
        serialized['founded'] = serialized.pop('founded').isoformat()
        serialized['createdAt'] = serialized.pop('createdAt').isoformat()
        serialized['updatedAt'] = serialized.pop('updatedAt').isoformat()

        return serialized

    @hybrid_property
    def getContacts(self) -> list[str]:
        """
        Parses the JSON string from the database and returns the changes as a dictionary.
        """

        return json.loads(str(self.contacts))

    @hybrid_property
    def logo_url(self) -> str:
        """Creates the URL for the team's logo."""

        if self.logo is None or self.logo == '':
            return ''

        match os.getenv('FLASK_ENV'):
            case 'development':
                return f'https://cdn.localhost/assets/{
                    PicturePathEnum.TEAM_PICTURES_FOLDER.value}/{
                    self.logo}'

            case 'production':
                return f'https://cdn.jugger-tourna.de/assets/{
                    PicturePathEnum.TEAM_PICTURES_FOLDER.value}/{
                    self.logo}'

            case _:
                return self.picture

    @logo_url.expression
    def logo_url(cls) -> Case:
        """Creates the URL for the team's logo."""

        return case(
            (cls.logo is None, literal(None)),
            (cls.logo == '', literal(None)),
            (literal(os.getenv('FLASK_ENV')) == 'development',
             literal(f'https://cdn.localhost/assets/{PicturePathEnum.TEAM_PICTURES_FOLDER.value}/') + cls.logo),
            (literal(os.getenv('FLASK_ENV')) == 'production',
             literal(
                 f'https://cdn.jugger-tourna.de/assets/{PicturePathEnum.TEAM_PICTURES_FOLDER.value}/') + cls.logo),
            else_=cls.logo
        )
