from dataclasses import dataclass
import json
import discord
import datetime


@dataclass
class Config:
    default_prefix: str
    case: int
    use_default_help: int
    owners: list[int]
    intents: str
    token: str
    version: str
    changelogs: dict[str, str | list[str]]
    what_am_i: str
    am_i_open_source: str
    git_repo: str
    help_text: str
    category_text: str


def parse_config() -> Config:
    """
    Run once at import-time.

    :return: Object representing configuration options
    :rtype: Config
    """

    with open("./config.json", "r") as handle:
        raw_config: dict = json.load(handle)

    if not isinstance(default_prefix := raw_config["default_prefix"], str):
        raise ValueError("default_prefix is non-str")

    if not isinstance(case := raw_config["case"], int):
        raise ValueError("case is non-int")

    if not isinstance(use_default_help := raw_config["use_default_help"], int):
        raise ValueError("use_default_help is non-int")

    if not isinstance(owners := raw_config["owners"], list):
        raise ValueError("owners is non-list")

    if not isinstance(intents := raw_config["intents"], str):
        raise ValueError("intents is non-str")

    if not isinstance(version := raw_config["version"], str):
        raise ValueError("version is non-str")

    if not isinstance(changelogs := raw_config["changelogs"], dict):
        raise ValueError("changelogs is non-dict")

    if not isinstance(what_am_i := raw_config["what_am_i"], str):
        raise ValueError("what_am_i is non-str")

    if not isinstance(am_i_open_source := raw_config["am_i_open_source"], str):
        raise ValueError("am_i_open_source is non-str")

    if not isinstance(git_repo := raw_config["git_repo"], str):
        raise ValueError("git_repo is non-str")

    if not isinstance(help_text := raw_config["help_text"], str):
        raise ValueError("help_text is non-str")

    if not isinstance(category_text := raw_config["category_text"], str):
        raise ValueError("category_text is non-str")

    with open("./token.txt", "r") as handle:
        token: str = handle.read().strip()

    return Config(
        default_prefix,
        case,
        use_default_help,
        owners,
        intents,
        token,
        version,
        changelogs,
        what_am_i,
        am_i_open_source,
        git_repo,
        help_text,
        category_text,
    )


def config_to_options() -> dict:
    options = {
        "command_prefix": config.default_prefix,  # TEMPORARY!
        "case_insensitive": bool(config.case),
        "owner_ids": set(config.owners),
    }

    intents = discord.Intents()

    match config.intents.lower():
        case "":
            options["intents"] = intents.none()
        case "default":
            options["intents"] = intents.default()
        case "all":
            options["intents"] = intents.all()

    if not config.use_default_help:
        options["help_command"] = None

    return options


config = parse_config()
start_time = datetime.datetime.now(datetime.timezone.utc)  # filled in by main.py
