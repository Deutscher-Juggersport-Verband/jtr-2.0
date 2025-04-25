from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import ToNullFilter
from flask_inputfilter.Validator import InEnumValidator

from DataDomain.Database.Enum import UserLanguageTypesEnum


class UpdateUserLanguageInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'language',
            required=True,
            filters=[
                ToNullFilter()
            ],
            validators=[
                InEnumValidator(
                    UserLanguageTypesEnum,
                )
            ]
        )
