import asyncio
from pathlib import Path
from discord.ext.commands import Bot


def load_cogs(bot: Bot):
    paths = Path("./commands").glob("*.py")
    cogs = [f"commands.{path.stem}" for path in paths]

    for cog in cogs:
        asyncio.run(bot.load_extension(cog))

    asyncio.run(bot.load_extension("jishaku"))
