from dataclasses import dataclass

from BusinessDomain.Tournament.Model import ResultElement


@dataclass
class CreateResultCommand:

    tournamentId: int
    resultElements: list[ResultElement]
