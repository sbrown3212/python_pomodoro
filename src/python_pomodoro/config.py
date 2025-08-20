import logging
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


logger = logging.getLogger(__name__)


# TODO: consider adding validation values (e.g. min and max, data types?)
CONFIG_SCHEMA = {
    "focus_duration": {
        "default": 25,
        "comment": "Focus session duration in minutes (int)",
    },
    "break_duration": {"default": 5, "comment": "Break duration in minutes (int)"},
    "auto_start_break": {
        "default": True,
        "comment": "Automatically start break when focus ends (bool)",
    },
    "auto_start_focus": {
        "default": False,
        "comment": "Automatically start focus when break ends (bool)",
    },
}


def get_config_path():
    return Path.home() / ".config" / "pmdro" / "config.toml"


def load_config_file():
    config_path = get_config_path()

    if not config_path.exists():
        return {}

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        logger.warning(f"Config file has invalid TOML syntax: {e}. Using defaults.")
        return {}
    except OSError as e:
        logger.warning(f"Could no read config file: {e}. Using defaults.")
        return {}


def get_defaults():
    defaults = {}
    for key, value in CONFIG_SCHEMA.items():
        defaults[key] = value["default"]

    return defaults


# TODO: change validation to be based on schema values.
def validate_config(config):
    max_timer = 180

    if config.get("focus_duration", 0) <= 0 or config.get("focus_duration") > max_timer:
        config["focus_duration"] = 25
    if config.get("break_duration", 0) <= 0 or config.get("break_duration") > max_timer:
        config["break_duration"] = 5
    if not isinstance(config.get("auto_start_break"), bool):
        config["auto_start_break"] = True
    if not isinstance(config.get("auto_start_focus"), bool):
        config["auto_start_focus"] = False

    return config


def get_effective_config():
    defaults = get_defaults()
    user_config = load_config_file()
    merged = {**defaults, **user_config}
    return validate_config(merged)


if __name__ == "__main__":
    print(get_defaults())
    print(get_effective_config())
