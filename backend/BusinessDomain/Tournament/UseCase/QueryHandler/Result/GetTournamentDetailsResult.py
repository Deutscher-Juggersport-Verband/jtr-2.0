from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from DataDomain.Database.Enum import (
    TournamentAccommodationTypesEnum,
    TournamentStatusTypesEnum,
)


@dataclass
class Accommodation:

    location: str
    type: TournamentAccommodationTypesEnum


@dataclass
class ArrivalDate:

    start: Optional[datetime]
    end: Optional[datetime]


@dataclass
class Costs:

    registrationCosts: float
    registrationCostsType: Optional[str]
    depositCosts: float
    depositCostsType: Optional[str]
    accommodationCosts: float
    accommodationCostsType: Optional[str]
    guestCosts: float
    guestCostsType: Optional[str]
    costsText: str


@dataclass
class Food:

    morning: str
    noon: str
    evening: str
    gastro: str


@dataclass
class HouseRules:

    text: str
    url: str


@dataclass
class Organizer:

    id: int
    name: str
    aboutUs: str
    city: str
    contacts: List[str]
    createdAt: datetime
    founded: Optional[str]
    isMixTeam: bool
    logo: str
    trainingTime: str
    updatedAt: datetime


@dataclass
class PompfCheck:

    text: str
    url: str


@dataclass
class RegistrationProcedure:

    text: str
    type: str
    url: str


@dataclass
class Shoes:

    barefootAllowed: bool
    camAllowed: bool
    cleatsAllowed: bool
    studdedAllowed: bool
    text: str


@dataclass
class TeamData:

    id: int
    name: str
    aboutUs: str
    city: str
    contacts: List[str]
    createdAt: datetime
    founded: Optional[str]
    isMixTeam: bool
    logo: str
    trainingTime: str
    updatedAt: datetime
    hasPayed: bool
    placement: Optional[int]
    registrationOrder: int


@dataclass
class Teams:

    participating: List[TeamData]
    waiting: List[TeamData]


@dataclass
class TournamentSystem:

    text: str
    url: str


@dataclass
class GetTournamentDetailsResult:

    id: int
    name: str
    accommodation: Accommodation
    additionalInformation: str
    address: str
    arrivalDate: ArrivalDate
    contacts: List[str]
    costs: Costs
    createdAt: datetime
    date: ArrivalDate
    deadlines: str
    food: Food
    houseRules: HouseRules
    location: str
    organizer: Organizer
    pompfCheck: PompfCheck
    possibleSpace: int
    registrationStartDate: str
    registrationProcedure: RegistrationProcedure
    schedule: Optional[str]
    shoes: Shoes
    status: TournamentStatusTypesEnum
    teamCount: int
    teams: Teams
    tournamentSystem: TournamentSystem
    updatedAt: datetime
