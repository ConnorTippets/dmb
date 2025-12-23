from discord.ext.commands import Cog, command, Context, Bot


class Fun(Cog):
    @command(brief="Says hello.")
    async def hello(self, ctx: Context):
        await ctx.send("Hello!")


async def setup(bot: Bot):
    await bot.add_cog(Fun(bot))
