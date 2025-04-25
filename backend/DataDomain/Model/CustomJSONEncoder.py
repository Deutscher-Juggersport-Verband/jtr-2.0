import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Row
from sqlalchemy.exc import OperationalError


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj) -> str | float | dict:

        if is_dataclass(obj):
            return asdict(obj)

        elif obj is None:
            return {}

        elif isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()

        elif isinstance(obj, Decimal):
            return float(obj)

        elif isinstance(obj, OperationalError):
            return str(obj)

        elif isinstance(obj, Row):
            return dict(obj._mapping)

        elif isinstance(obj, Enum):
            return obj.value

        return super().default(obj)
