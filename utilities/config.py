from dataclasses import dataclass
import json
import discord


@dataclass
class Config:
    default_prefix: str
    case: int
    use_default_help: int
    owners: list[int]
    intents: str
    token: str
    version: str
    whatami: str
    amiopensource: str
    gitrepo: str


def parse_config() -> Config:
    """
    Run once at import-time.

    :return: Object representing configuration options
    :rtype: Config
    """

    with open("./config.json", "r") as handle:
        raw_config: dict[str, str | int | list[int]] = json.load(handle)

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

    if not isinstance(whatami := raw_config["whatami"], str):
        raise ValueError("whatami is non-str")

    if not isinstance(amiopensource := raw_config["amiopensource"], str):
        raise ValueError("amiopensource is non-str")

    if not isinstance(gitrepo := raw_config["gitrepo"], str):
        raise ValueError("gitrepo is non-str")

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
        whatami,
        amiopensource,
        gitrepo,
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
