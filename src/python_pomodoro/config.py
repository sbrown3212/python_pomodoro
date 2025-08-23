import logging
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


logger = logging.getLogger(__name__)


# TODO: consider adding validation values (e.g. min and max, data types?)
# Validation types:
# - type
# - min
# - max
#
CONFIG_SCHEMA = {
    "focus_duration": {
        "default": 25,
        "comment": "Focus session duration in minutes (int)",
        "validation": {
            "type": int,
            "min": 1,
            "max": 480,
        },
    },
    "break_duration": {
        "default": 5,
        "comment": "Break duration in minutes (int)",
        "validation": {
            "type": int,
            "min": 1,
            "max": 480,
        },
    },
    "auto_start_break": {
        "default": True,
        "comment": "Automatically start break when focus ends (bool)",
        "validation": {
            "type": bool,
        },
    },
    "auto_start_focus": {
        "default": False,
        "comment": "Automatically start focus when break ends (bool)",
        "validation": {
            "type": bool,
        },
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


# # Alternatively, here is the same thing as a dictionary comprehension.
# def get_defaults():
#     return {key: config["default"] for key, config in CONFIG_SCHEMA.items()}
def get_defaults():
    defaults = {}
    for key, value in CONFIG_SCHEMA.items():
        defaults[key] = value["default"]

    return defaults


# TODO: change validation to be based on schema values.
def validate_config(config):
    # max_timer = 180
    #
    # if config.get("focus_duration", 0) <= 0 or config.get("focus_duration") > max_timer:
    #     config["focus_duration"] = 25
    # if config.get("break_duration", 0) <= 0 or config.get("break_duration") > max_timer:
    #     config["break_duration"] = 5
    # if not isinstance(config.get("auto_start_break"), bool):
    #     config["auto_start_break"] = True
    # if not isinstance(config.get("auto_start_focus"), bool):
    #     config["auto_start_focus"] = False
    #
    # return config
    for schema_key, schema_item in CONFIG_SCHEMA.items():
        if schema_key in config:
            value = config[schema_key]

            rules = CONFIG_SCHEMA[schema_key]["validation"]

            expected_type = rules["type"]
            if not isinstance(value, expected_type):
                logger.warning(
                    f"Config key '{schema_key}' is not of type '{rules['type'].__name__}'. Using default."
                )
                config[schema_key] = schema_item["default"]
                continue

            if "min" in rules and value < rules["min"]:
                logger.warning(
                    f"Config key '{schema_key}' is below the minimum value of {rules['min']}. Using default."
                )
                config[schema_key] = schema_item["default"]

            if "max" in rules and value > rules["max"]:
                logger.warning(
                    f"Config key '{schema_key}' is above the maximum value of {rules['max']}. Using default."
                )
                config[schema_key] = schema_item["default"]

        else:
            config[schema_key] = schema_item["default"]

    for key in config:
        if key not in CONFIG_SCHEMA:
            logger.warning(f"Unknown key '{key}' in config. Ignoring value.")

    return config


def get_effective_config():
    defaults = get_defaults()
    user_config = load_config_file()
    merged = {**defaults, **user_config}
    return validate_config(merged)


if __name__ == "__main__":
    print(get_defaults())
    print(get_effective_config())
