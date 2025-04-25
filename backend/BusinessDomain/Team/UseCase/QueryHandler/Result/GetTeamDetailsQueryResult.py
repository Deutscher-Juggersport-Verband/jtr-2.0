from dataclasses import dataclass
from datetime import datetime

from BusinessDomain.Team.Model import OrganizedTournamentsModel, PastTournamentsModel
from BusinessDomain.Team.UseCase.QueryHandler.Result import MembersResult


@dataclass
class GetTeamDetailsQueryResult:

    id: int
    aboutUs: str | None
    city: str | None
    contacts: list[str]
    escapedName: str
    founded: datetime
    isMixTeam: bool | None
    lastOrganizedTournament: datetime | None
    lastParticipatedTournament: datetime | None
    logoUrl: str
    members: list[MembersResult]
    name: str
    organizedTournaments: list[OrganizedTournamentsModel]
    pastTournaments: list[PastTournamentsModel]
    points: float
    trainingTime: str | None
    trainingTimeUpdatedAt: datetime | None
