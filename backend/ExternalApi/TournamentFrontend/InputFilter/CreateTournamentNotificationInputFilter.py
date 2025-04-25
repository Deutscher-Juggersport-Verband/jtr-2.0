from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import ToIntegerFilter, ToStringFilter
from flask_inputfilter.Validator import IsIntegerValidator, IsStringValidator


class CreateTournamentNotificationInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'tournamentId',
            required=True,
            filters=[
                ToIntegerFilter()
            ],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'message',
            required=True,
            filters=[
                ToStringFilter()
            ],
            validators=[
                IsStringValidator()
            ]
        )
