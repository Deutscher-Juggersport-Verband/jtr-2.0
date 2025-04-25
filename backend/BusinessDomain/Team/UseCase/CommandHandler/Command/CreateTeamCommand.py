from dataclasses import dataclass


@dataclass
class CreateTeamCommand:

    aboutUs: str | None
    city: str | None
    contacts: list[str] | None
    escapedName: str
    isMixTeam: bool | None
    name: str
    trainingTime: str | None
