from discord.ext.commands import Cog, command, Context, Bot, is_owner, ExtensionFailed
import traceback


class Debug(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="Reloads a cog.")
    @is_owner()
    async def reload_extension(self, ctx: Context, *, extension: str):
        try:
            if not extension == "jishaku":
                extension = f"commands.{extension}"
            await self.bot.reload_extension(extension)
            await ctx.message.add_reaction("\U00002705")
        except ExtensionFailed as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            await ctx.send(f"```py\n{tb}```")


async def setup(bot: Bot):
    await bot.add_cog(Debug(bot))
