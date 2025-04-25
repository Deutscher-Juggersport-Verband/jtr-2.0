from flask_inputfilter import InputFilter
from flask_inputfilter.Enum.RegexEnum import RegexEnum
from flask_inputfilter.Filter import (
    StringTrimFilter,
    ToBooleanFilter,
    ToIntegerFilter,
    ToNullFilter,
)
from flask_inputfilter.Validator import (
    InEnumValidator,
    IsArrayValidator,
    IsBooleanValidator,
    IsIntegerValidator,
    IsStringValidator,
    RegexValidator,
)

from DataDomain.Database.Enum import (
    TournamentAccommodationTypesEnum,
    TournamentCostTypesEnum,
    TournamentFoodEveningTypesEnum,
    TournamentFoodGastroTypesEnum,
    TournamentFoodMorningTypesEnum,
    TournamentFoodNoonTypesEnum,
    TournamentRegistrationProcedureTypesEnum,
)


class UpdateTournamentInputFilter(InputFilter):

    def __init__(self) -> None:

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
            'additionalInformation',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'name',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'startDate',
            required=True,
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATE.value,
                    'Das Startdatum muss im iso format sein.'
                )
            ]
        )

        self.add(
            'endDate',
            required=True,
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATE.value,
                    'Das Enddatum muss im iso format sein.'
                )
            ]
        )

        self.add(
            'startArrivalDate',
            required=False,
            filters=[ToNullFilter()],
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATE.value,
                    'Das StartAnkunftsdatum muss im iso format sein.'
                )
            ]
        )

        self.add(
            'endArrivalDate',
            required=False,
            filters=[ToNullFilter()],
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATE.value,
                    'Das EndAnkunftsdatum muss im iso format sein.'
                )
            ]
        )

        self.add(
            'address',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'possibleSpace',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )

        self.add(
            'registrationProcedureType',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentRegistrationProcedureTypesEnum
                )
            ]
        )

        self.add(
            'registrationProcedureText',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'registrationStartDate',
            required=True,
            validators=[
                RegexValidator(
                    RegexEnum.ISO_DATE.value,
                    'Das Anmeldedatum muss im iso format sein.'
                )
            ]
        )

        self.add(
            'registrationCosts',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )

        self.add(
            'registrationCostsType',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[
                InEnumValidator(
                    TournamentCostTypesEnum
                )
            ]
        )

        self.add(
            'depositCosts',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )

        self.add(
            'depositCostsType',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[
                InEnumValidator(
                    TournamentCostTypesEnum
                )
            ]
        )

        self.add(
            'accommodationCosts',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'accommodationCostsType',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[
                InEnumValidator(
                    TournamentCostTypesEnum
                )
            ]
        )

        self.add(
            'guestCosts',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator()
            ]
        )

        self.add(
            'guestCostsType',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[
                InEnumValidator(
                    TournamentCostTypesEnum
                )
            ]
        )

        self.add(
            'costsText',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'deadlines',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'schedule',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'contacts',
            required=True,
            validators=[IsArrayValidator()],
        )

        self.add(
            'accommodationType',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentAccommodationTypesEnum
                )
            ]
        )

        self.add(
            'accommodationLocation',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'location',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'foodMorning',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentFoodMorningTypesEnum
                )
            ]
        )

        self.add(
            'foodNoon',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentFoodNoonTypesEnum
                )
            ]
        )

        self.add(
            'foodEvening',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentFoodEveningTypesEnum
                )
            ]
        )

        self.add(
            'foodGastro',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                InEnumValidator(
                    TournamentFoodGastroTypesEnum
                )
            ]
        )

        self.add(
            'tournamentSystemText',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'tournamentSystemUrl',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'pompfCheckText',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'pompfCheckUrl',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'houseRulesText',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'houseRulesUrl',
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'studdedShoesAllowed',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
        )

        self.add(
            'cleatsShoesAllowed',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
        )

        self.add(
            'camShoesAllowed',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
        )

        self.add(
            'barefootAllowed',
            required=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()]
        )

        self.add(
            'shoesText',
            required=False,
            filters=[StringTrimFilter(), ToNullFilter()],
            validators=[IsStringValidator()]
        )
