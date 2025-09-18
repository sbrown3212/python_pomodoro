import logging
import time
from enum import Enum
from dataclasses import dataclass

# from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class TimerStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


class SessionType(Enum):
    FOCUS = "focus"
    BREAK = "break"


class TimeStamp:
    def __init__(self, value: int):
        self.value = value

    @classmethod
    def now(cls):
        return cls(int(time.time()))

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, TimeStamp) and self.value == other.value


STATE_SCHEMA = {
    "status": {
        "type": TimerStatus,
        "required_for": {
            TimerStatus.IDLE,
            TimerStatus.RUNNING,
            TimerStatus.PAUSED,
            TimerStatus.COMPLETED,
        },
        "cleared_value": TimerStatus.IDLE,
    },
    "session_type": {
        "type": SessionType,
        "required_for": {
            TimerStatus.RUNNING,
            TimerStatus.PAUSED,
            TimerStatus.COMPLETED,
        },
        "cleared_value": None,
    },
    "start_time": {
        "type": TimeStamp,
        "required_for": {
            TimerStatus.RUNNING,
            TimerStatus.PAUSED,
            TimerStatus.COMPLETED,
        },
        "cleared_value": None,
    },
    "duration_minutes": {
        "type": int,
        "required_for": {
            TimerStatus.RUNNING,
            TimerStatus.PAUSED,
            TimerStatus.COMPLETED,
        },
        "cleared_value": 0,
    },
    "pause_time": {
        "type": TimeStamp,
        "required_for": {TimerStatus.PAUSED},
        "cleared_value": None,
    },
    "total_paused_seconds": {
        "type": int,
        "required_for": {TimerStatus.PAUSED},  # is this required for 'completed'?
        "cleared_value": 0,
    },
}


REQUIRED_FIELDS = {
    TimerStatus.IDLE: {},
    TimerStatus.RUNNING: {"status", "session_type", "start_time", "duration_minutes"},
    TimerStatus.PAUSED: {
        "status",
        "session_type",
        "start_time",
        "duration_minutes",
        "pause_time",
        "total_paused_seconds",
    },
}


@dataclass
class Timer:
    status: TimerStatus
    session_type: Optional[SessionType]
    start_time: Optional[int] = None
    duration_minutes: Optional[int] = None
    pause_time: Optional[int] = None
    total_paused_seconds: int = 0

    def __post_init__(self):
        # QUESTION: Is it better (simpler or more performant) to have a main loop or branching?
        if self.status is TimerStatus.IDLE:
            # Clear all values
            for schema_key in STATE_SCHEMA:
                self._clear_field(schema_key)

            return

        elif self.status is TimerStatus.RUNNING:
            # Iterate over schema fields
            # -- Skip "status" field
            # -- Require all required fields
            # -- Validate required values values
            for schema_key, schema_value in STATE_SCHEMA.items():
                if schema_key == "status":
                    continue

                if schema_key in REQUIRED_FIELDS[self.status]:
                    self._require_field(schema_key)

                    field_type = getattr(self, schema_key)

                    if field_type == TimeStamp:
                        self._validate_timestamp(schema_key)
                    elif field_type is int:
                        self._validate_non_negative_int(schema_key, False)
                    elif field_type == SessionType:
                        # TODO: implement validation for 'SessionType'???
                        pass

        elif self.status is TimerStatus.PAUSED:
            pass

        else:  # completed
            pass

        # for schema_key, value_dict in STATE_SCHEMA.items():
        #     if schema_key == "status":
        #         continue
        #
        #     # current_value = getattr(self, schema_key)
        #
        #     # Clear value if not required for current status
        #     required_status_set = getattr(value_dict, "required_for")
        #     if self.status not in required_status_set:
        #         # TODO: update _log_and_clear to use STATE_SCHEMA 'cleared_value'
        #         self._clear_field(schema_key)
        #         continue
        #
        #     # Clear if field is ???
        #     #

    def _log_and_clear(self, field_name: str):
        # TODO: update _log_and_clear to use STATE_SCHEMA 'cleared_value'
        current_value = getattr(self, field_name)
        target_value = 0 if isinstance(current_value, int) else None

        if current_value == target_value:
            return

        setattr(self, field_name, target_value)

        logger.warning(
            f"Auto-cleaned '{field_name}' from '{current_value}' to '{target_value}'."
        )

    def _validate_timestamp(self, field_name: str):
        # TODO: update this method to use new 'TimeStamp' class
        timestamp = getattr(self, field_name)
        if timestamp is None:
            return

        if not isinstance(timestamp, int):
            raise ValueError(f"Invalid {field_name}: timestamp must be of type 'int'.")

        current_time = int(time.time())
        if timestamp >= current_time:
            raise ValueError(f"Invalid {field_name}: timestamp is in the future.")
        elif current_time - timestamp > 86400:
            raise ValueError(
                f"Invalid {field_name}: timestamp is more than 24 hours old."
            )

    def _validate_non_negative_int(self, field_name: str, allow_zero: bool):
        # TODO: update this method (and method name) to only allow positive (non-zero) nums
        current_int = getattr(self, field_name)

        if current_int is None:
            return

        if not isinstance(current_int, int):
            raise ValueError(f"Invalid {field_name}: value must be of type 'int'.")

        if allow_zero and current_int < 0:
            raise ValueError(
                f"Invalid {field_name}: value must be greater than or equal to zero."
            )
        elif not allow_zero and current_int <= 0:
            raise ValueError(f"Invalid {field_name}: value must be greater than zero.")

    def _require_field(self, field_name: str):
        current_value = getattr(self, field_name)

        if current_value is None:
            raise ValueError(f"{field_name} is required for {self.status.value} state.")

    def _clear_field(self, field_name: str):
        target_value = STATE_SCHEMA[field_name]["cleared_value"]
        setattr(self, field_name, target_value)

    def _validate_field(self, field_name: str):
        current_value = getattr(self, field_name)

        if not isinstance(current_value, STATE_SCHEMA[field_name]["type"]):
            raise TypeError(
                f"{field_name} should be of type {STATE_SCHEMA[field_name]['type']}, but is currently {type(current_value)}."
            )

        if isinstance(current_value, int):
            # Ensure int value is positive (should 0 be allowed?
            # Are 'total_paused_seconds' and 'duration_minutes' going to be checked always?)
            pass

        elif isinstance(current_value, TimeStamp):
            # QUESTION: Is here where I should ensure that there are no future timestamps and no timestamps older than 24 hours?
            pass


def get_state_path():
    pass


def load_state():
    pass


def save_state():
    pass


def clear_state():
    pass
