from flask_inputfilter import InputFilter
from flask_inputfilter.Enum.RegexEnum import RegexEnum
from flask_inputfilter.Filter import StringTrimFilter, ToBooleanFilter, ToNullFilter
from flask_inputfilter.Validator import (
    IsBooleanValidator,
    IsStringValidator,
    RegexValidator,
)


class CreateUserInputFilter(InputFilter):

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
            'isBirthdateVisible',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
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
            'isCityVisible',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
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
            'isNameVisible',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
        )

        self.add(
            'password',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'username',
            required=True,
            filters=[
                StringTrimFilter()
            ],
            validators=[IsStringValidator()]
        )

        self.add(
            'language',
            required=False,
            filters=[
                StringTrimFilter()
            ],
            validators=[IsStringValidator()]
        )
