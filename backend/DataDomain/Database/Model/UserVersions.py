import json
from datetime import datetime
from typing import Any, Self

from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

from DataDomain.Database import db
from DataDomain.Database.Model import BaseModel


class UserVersions(BaseModel, db.Model):

    __tablename__ = 'user_versions'

    id: int = db.Column(
        db.Integer,
        primary_key=True
    )

    version: int = db.Column(
        db.Integer,
        nullable=False
    )

    changes: str = db.Column(
        'changes',
        db.JSON,
        nullable=False
    )

    updated_at: datetime = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )

    def serialize(self) -> dict[str, Any]:
        """
        Serializes the object as a dictionary.
        """

        serialized = super().serialize()

        serialized['changes'] = self.getChanges

        return serialized

    @hybrid_property
    def getChanges(self) -> dict[str, Any]:
        """
        Parses the JSON string from the database and returns the changes as a dictionary.
        """

        return json.loads(self.changes)

    def setChanges(self, changesDict: dict[str, Any]) -> Self:
        """
        Takes the dictionary and safes it as a JSON-String in the 'changes' column.
        """

        self.changes = json.dumps(changesDict)

        return self
