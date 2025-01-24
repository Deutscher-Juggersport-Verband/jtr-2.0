from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import StringTrimFilter
from flask_inputfilter.Validator import IsStringValidator


class CreatePasswordResetInputFilter(InputFilter):
    """The input filter for the create-password-reset route"""

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'email',
            required=True,
            filters=[
                StringTrimFilter()
            ],
            validators=[IsStringValidator()]
        )
