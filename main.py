import discord
import os
from discord.ext.commands import (
    Bot,
    Context,
    CommandError,
    CommandNotFound,
    CheckFailure,
    is_owner,
    ExtensionFailed,
)
from utilities.config import config, config_to_options, start_time
from utilities.cogs import load_cogs
import traceback
import datetime

bot = Bot(**config_to_options())
load_cogs(bot)
os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"
os.environ["JISHAKU_HIDE"] = "true"


@bot.event
async def on_command_error(ctx: Context, exception: CommandError):
    embed = discord.Embed(title="Error", color=0xE33232)

    supress_log = [
        CheckFailure,
    ]

    if not isinstance(exception, CommandNotFound):
        embed.description = str(exception)
        await ctx.send(embed=embed)

        if any(isinstance(exception, typ) for typ in supress_log):
            return

        # for logging the error
        await Bot.on_command_error(bot, ctx, exception)


@bot.command(brief="Reloads a cog.")
@is_owner()
async def reload_extension(ctx: Context, *, extension: str):
    try:
        if not extension == "jishaku":
            extension = f"commands.{extension}"
        await bot.reload_extension(extension)
        await ctx.message.add_reaction("\U00002705")
    except ExtensionFailed as e:
        tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        await ctx.send(f"```py\n{tb}```")


@bot.command(brief="Restarts the bot.")
@is_owner()
async def restart(ctx: Context):
    os.system(rf"cmd /c taskkill /F /PID {os.getpid()} && .\main.py")


@bot.event
async def on_ready():
    start_time = datetime.datetime.now(datetime.timezone.utc)


bot.run(config.token)
