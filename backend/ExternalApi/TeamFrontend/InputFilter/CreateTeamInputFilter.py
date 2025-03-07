from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import StringTrimFilter, ToBooleanFilter, ToNullFilter
from flask_inputfilter.Validator import (
    IsArrayValidator,
    IsBooleanValidator,
    IsStringValidator,
)


class CreateTeamInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'name',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
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
            validators=[IsArrayValidator()]
        )
