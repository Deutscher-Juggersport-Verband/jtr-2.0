from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import ToIntegerFilter, ToNullFilter
from flask_inputfilter.Validator import IsIntegerValidator


class DeleteMembershipInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'teamId',
            required=True,
            filters=[
                ToIntegerFilter()
            ],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'userId',
            required=False,
            filters=[
                ToIntegerFilter(),
                ToNullFilter()
            ],
            validators=[
                IsIntegerValidator()
            ]
        )
