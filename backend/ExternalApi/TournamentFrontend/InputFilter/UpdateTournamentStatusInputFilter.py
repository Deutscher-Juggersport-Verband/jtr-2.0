from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import StringTrimFilter, ToIntegerFilter
from flask_inputfilter.Validator import InEnumValidator, IsIntegerValidator

from DataDomain.Database.Enum import TournamentStatusTypesEnum


class UpdateTournamentStatusInputFilter(InputFilter):
    """The input filter for the update-tournament-status route"""

    def __init__(self):
        """Initializes the UpdateTournamentStatusInputFilter"""

        super().__init__()

        self.add(
            'tournamentId',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'status',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentStatusTypesEnum
                )
            ]
        )
