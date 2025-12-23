import discord
import asyncio
from discord.ext.commands import (
    Bot,
    Context,
    CommandError,
    CommandNotFound,
    CheckFailure,
)
from utilities.config import config, config_to_options

bot = Bot(**config_to_options())
asyncio.run(bot.load_extension("commands.fun"))


@bot.event
async def on_command_error(ctx: Context, exception: CommandError):
    embed = discord.Embed(title="Error", color=0xE33232)

    if isinstance(exception, CheckFailure):
        embed.description = f"You do not have the permission to run this command.\n{type(exception).__name__}"
    elif isinstance(exception, CommandNotFound):
        return
    else:
        embed.description = str(exception)

    await ctx.send(embed=embed)

    # for logging the error
    await bot.on_command_error(ctx, exception)  # this SHOULD call the original func?


bot.run(config.token)
