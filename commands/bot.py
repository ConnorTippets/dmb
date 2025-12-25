from discord import Embed
from discord.ext.commands import (
    Cog,
    command,
    Context,
    Bot as B,
    Paginator,
    Command,
    CheckFailure,
)
from utilities.config import config, start_time
from jishaku.paginators import PaginatorEmbedInterface
import typing
import datetime
import humanize
import difflib


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

    async def can_run(self, ctx: Context, command: Command) -> bool:
        try:
            return await command.can_run(ctx)
        except CheckFailure:
            return False

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
            value=config.what_am_i.format(app_info.owner.mention),
            inline=False,
        )
        embed.add_field(
            name="Am I open source?",
            value=config.am_i_open_source.format(config.git_repo),
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

    @command(brief="Display help for DMB.")
    async def help(self, ctx: Context, *, query: str | None = None):
        embed = Embed(color=0x2F3136)

        cogs = self.bot.cogs

        if not query:
            embed.title = "Help Categories"

            categories = list(cogs)
            categories.remove("Jishaku")

            embed.add_field(
                name="Categories",
                value=config.help_text.format("\n".join(categories), ctx.prefix),
            )

            return await ctx.send(embed=embed)

        query = query.lower()

        queried_command = self.bot.get_command(query)

        if queried_command:
            if not await self.can_run(ctx, queried_command):
                embed.title = "You do not have the permission to view this command."
                embed.color = 0xE33232

                return await ctx.send(embed=embed)

            # fallback incase brief is none
            command_help = (
                queried_command.brief
                or queried_command.description
                or queried_command.help
            )

            embed.title = queried_command.qualified_name
            embed.add_field(
                name="Description",
                value=f"```\n{command_help}\n```",
                inline=False,
            )
            embed.add_field(
                name="Usage",
                value=f"```\n{queried_command.qualified_name} {queried_command.signature}\n```",
                inline=False,
            )

            return await ctx.send(embed=embed)

        queried_cog = cogs.get(query.capitalize(), None)

        if queried_cog:
            embed.title = queried_cog.qualified_name

            commands = [
                command.name if not command.root_parent else command.qualified_name
                for command in queried_cog.walk_commands()
                if await self.can_run(ctx, command)
            ]

            embed.add_field(
                name="Commands",
                value=config.category_text.format("\n".join(commands), ctx.prefix),
            )

            return await ctx.send(embed=embed)

        command_matches = set(
            difflib.get_close_matches(
                query, [command.name for command in self.bot.commands]
            )
        )
        command_matches = command_matches | set(
            difflib.get_close_matches(
                query, [command.qualified_name for command in self.bot.commands]
            )
        )

        cog_matches = set(difflib.get_close_matches(query, self.bot.cogs))

        for name in command_matches:
            command = self.bot.get_command(name)

            if not command:
                continue

            if not self.can_run(ctx, command):
                command_matches.remove(name)

        embed.title = "Query not found"
        embed.color = 0xE33232

        if command_matches or cog_matches:
            embed.add_field(
                name="Possible Matches",
                value=f"```\n{"\n".join(command_matches)}\n{"\n".join(cog_matches)}\n```",
            )
        else:
            embed.description = "No possible matches found."

        return await ctx.send(embed=embed)


async def setup(bot: B):
    await bot.add_cog(Bot(bot))
