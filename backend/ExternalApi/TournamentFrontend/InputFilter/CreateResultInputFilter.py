from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import ToIntegerFilter
from flask_inputfilter.Validator import (
    ArrayElementValidator,
    IsArrayValidator,
    IsIntegerValidator,
)


class CreateResultInputFilter(InputFilter):

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

        resultElementFilter = InputFilter()
        resultElementFilter.add(
            'teamId',
            required=True,
            filters=[
                ToIntegerFilter()
            ],
            validators=[
                IsIntegerValidator()
            ]
        )
        resultElementFilter.add(
            'placement',
            required=True,
            filters=[
                ToIntegerFilter()
            ],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'resultElements',
            required=True,
            validators=[
                IsArrayValidator(),
                ArrayElementValidator(
                    resultElementFilter
                )
            ]
        )
