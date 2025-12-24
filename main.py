import discord
from discord.ext.commands import (
    Bot,
    Context,
    CommandError,
    CommandNotFound,
    CheckFailure,
)
from utilities.config import config, config_to_options
from utilities.cogs import load_cogs

bot = Bot(**config_to_options())
load_cogs(bot)


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


bot.run(config.token)
