from flask import current_app
from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import ToIntegerFilter
from flask_inputfilter.Validator import (
    IsBase64ImageCorrectSizeValidator,
    IsBase64ImageValidator,
    IsIntegerValidator,
)


class UpdateTeamPictureInputFilter(InputFilter):

    def __init__(self) -> None:

        super().__init__()

        self.add(
            'teamId',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )

        self.add(
            'picture',
            required=True,
            validators=[
                IsBase64ImageValidator(),
                IsBase64ImageCorrectSizeValidator(
                    minSize=1,
                    maxSize=current_app.config['MAX_CONTENT_LENGTH'])])
