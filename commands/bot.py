from discord import Embed
from discord.ext.commands import Cog, command, Context, Bot as B
from utilities.config import config


class Bot(Cog):
    def __init__(self, bot: B):
        self.bot = bot

    @command(brief="Information about DMB.")
    async def about(self, ctx: Context):
        if not (self.bot.user and self.bot.user.avatar):
            return

        app_info = await self.bot.application_info()

        embed = Embed(title="About DMB", color=0x2F3136)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Version", value=config.version, inline=False)
        embed.add_field(
            name="What am I?",
            value=config.whatami.format(app_info.owner.mention),
            inline=False,
        )
        embed.add_field(
            name="Am I open source?", value=config.amiopensource.format(config.gitrepo)
        )
        embed.set_footer(
            text=f"DMB version {config.version}", icon_url=self.bot.user.avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: B):
    await bot.add_cog(Bot(bot))
