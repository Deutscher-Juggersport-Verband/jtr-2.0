from flask_inputfilter import InputFilter
from flask_inputfilter.Enum.RegexEnum import RegexEnum
from flask_inputfilter.Filter import (
    StringTrimFilter,
    ToBooleanFilter,
    ToIntegerFilter,
    ToNullFilter,
)
from flask_inputfilter.Validator import (
    IsArrayValidator,
    IsBooleanValidator,
    IsIntegerValidator,
    IsStringValidator,
    RegexValidator,
)


class UpdateTeamInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'teamId',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'name',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'logo',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'founded',
            required=False,
            filters=[
                ToNullFilter()
            ],
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATETIME.value,
                )
            ]
        )

        self.add(
            'city',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'isMixTeam',
            required=False,
            filters=[ToBooleanFilter(), ToNullFilter()],
            validators=[IsBooleanValidator()]
        )

        self.add(
            'trainingTime',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'aboutUs',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'contacts',
            required=False,
            filters=[ToNullFilter()],
            validators=[IsArrayValidator()],
        )
