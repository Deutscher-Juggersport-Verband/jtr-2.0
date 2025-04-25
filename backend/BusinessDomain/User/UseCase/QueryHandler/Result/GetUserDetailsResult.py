from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class TeamResult:

    id: int
    escapedName: str
    logoUrl: str
    name: str


@dataclass
class GetUserDetailsResult:

    id: int
    createdAt: datetime
    email: str
    isBirthdateVisible: bool
    isCityVisible: bool
    isDeleted: bool
    isNameVisible: bool
    pictureUrl: str
    pronouns: str
    teams: list[TeamResult]
    updatedAt: datetime
    username: str
    name: str | None = None
    birthdate: date | None = None
    city: str | None = None
