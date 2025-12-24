from discord import Embed
from discord.ext.commands import Cog, command, Context, Bot as B, Paginator
from utilities.config import config, start_time
from jishaku.paginators import PaginatorEmbedInterface
import typing
import datetime
import humanize


class ChangelogPaginator(PaginatorEmbedInterface):
    @property
    def send_kwargs(self) -> dict[str, typing.Any]:
        version = list(config.changelogs.keys())[self.display_page]

        title = f"Version {version}"
        if version == "Older Versions":
            title = version

        self._embed.title = title
        self._embed.description = self.pages[self.display_page]

        return {"embed": self._embed, "view": self}


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

    @command(brief="Information about DMB's running instance.")
    async def status(self, ctx: Context):
        if not (self.bot.user and self.bot.user.avatar):
            return

        runtime = datetime.datetime.now(datetime.timezone.utc)

        message = await ctx.send("TEST")

        total_latency = humanize.precisedelta(
            datetime.datetime.now(datetime.timezone.utc) - runtime,
            minimum_unit="milliseconds",
            format="%0.0f",
        )

        uptime = humanize.precisedelta(
            runtime - start_time,
            minimum_unit="seconds",
            format="%0.0f",
        )

        api_latency = f"{int(self.bot.latency * 1000)}ms"

        embed = Embed(title="Bot Status", color=0x2F3136)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Uptime", value=uptime, inline=False)
        embed.add_field(name="Total Latency", value=total_latency, inline=True)
        embed.add_field(name="API Latency", value=api_latency, inline=True)
        embed.set_footer(
            text=f"DMB version {config.version}", icon_url=self.bot.user.avatar.url
        )

        await message.edit(content="", embed=embed)

    @command(brief="Information about changes in DMB.")
    async def changelog(self, ctx: Context):
        paginator = Paginator(max_size=1900)

        paginator._pages = [
            "\n".join(ver) if isinstance(ver, list) else ver
            for ver in config.changelogs.values()
        ]

        embed = Embed(title=f"Version {config.version}", color=0x2F3136)
        interface = ChangelogPaginator(
            self.bot, paginator, owner=ctx.author, embed=embed
        )

        await interface.send_to(ctx)


async def setup(bot: B):
    await bot.add_cog(Bot(bot))
