import logging
import time
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
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


@dataclass
class Timer:
    status: TimerStatus
    session_type: Optional[SessionType]
    start_time: Optional[int] = None
    duration_minutes: Optional[int] = None
    pause_time: Optional[int] = None
    total_paused_seconds: int = 0

    def __post_init__(self):
        if self.status is TimerStatus.IDLE:
            pass

        elif self.status is TimerStatus.RUNNING:
            pass

        elif self.status is TimerStatus.PAUSED:
            pass

        else:  # completed
            pass

    def _log_and_clear(self, field_name: str):
        current_value = getattr(self, field_name)
        target_value = 0 if isinstance(current_value, int) else None

        if current_value == target_value:
            return

        setattr(self, field_name, target_value)

        logger.warning(
            f"Auto-cleaned '{field_name}' from '{current_value}' to '{target_value}'."
        )

    def _validate_timestamp(self, field_name: str):
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


def get_state_path():
    pass


def load_state():
    pass


def save_state():
    pass


def clear_state():
    pass
