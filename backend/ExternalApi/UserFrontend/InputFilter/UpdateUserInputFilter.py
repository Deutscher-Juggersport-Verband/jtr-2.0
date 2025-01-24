from flask_inputfilter import InputFilter
from flask_inputfilter.Enum.RegexEnum import RegexEnum
from flask_inputfilter.Filter import StringTrimFilter, ToNullFilter
from flask_inputfilter.Validator import (
    IsBooleanValidator,
    IsStringValidator,
    RegexValidator,
)


class UpdateUserInputFilter(InputFilter):
    """The input filter for the update-user route"""

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'birthdate',
            required=False,
            filters=[
                ToNullFilter()
            ],
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATE.value,
                    'Das Geburtsdatum muss im iso format sein.'
                )
            ]
        )

        self.add(
            'city',
            required=False,
            filters=[
                StringTrimFilter(),
                ToNullFilter()
            ],
            validators=[IsStringValidator()]
        )

        self.add(
            'email',
            required=False,
            filters=[
                StringTrimFilter(),
                ToNullFilter()
            ],
            validators=[
                RegexValidator(
                    RegexEnum.EMAIL.value,
                    'Die Email muss das Format einer Email haben.'
                )
            ]
        )

        self.add(
            'name',
            required=False,
            filters=[
                StringTrimFilter(),
                ToNullFilter()
            ],
            validators=[IsStringValidator()]
        )

        self.add(
            'password',
            required=False,
            filters=[
                StringTrimFilter(),
                ToNullFilter()
            ],
            validators=[IsStringValidator()]
        )

        self.add(
            'pronouns',
            required=False,
            filters=[
                StringTrimFilter(),
                ToNullFilter()
            ],
            validators=[IsStringValidator()]
        )

        self.add(
            'username',
            required=False,
            filters=[
                StringTrimFilter(),
                ToNullFilter()
            ],
            validators=[IsStringValidator()]
        )

        self.add(
            'isBirthdateVisible',
            required=True,
            validators=[IsBooleanValidator()]
        )

        self.add(
            'isCityVisible',
            required=True,
            validators=[IsBooleanValidator()]
        )

        self.add(
            'isNameVisible',
            required=True,
            validators=[IsBooleanValidator()]
        )
