from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import ToIntegerFilter
from flask_inputfilter.Validator import IsIntegerValidator


class SendTeamInvitationInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'userId',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )

        self.add(
            'teamId',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )
