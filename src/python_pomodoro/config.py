from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def get_config_path():
    return Path.home() / ".config" / "pmdro" / "config.toml"


def load_config_file():
    config_path = get_config_path()

    if not config_path.exists():
        return {}

    with open(config_path, "rb") as f:
        return tomllib.load(f)


def get_defaults():
    return {
        "focus_duration": 25,
        "break_duration": 5,
        "auto_start_break": True,
        "auto_start_focus": False,
    }


def get_effective_config():
    defauts = get_defaults()
    user_config = load_config_file()
    return {**defauts, **user_config}


if __name__ == "__main__":
    print(get_effective_config())
