from discord.ext import commands
from database import User, GuildData, Log
from datetime import datetime
from pytz import timezone
from discord import Member, TextChannel


class Config(commands.Cog):
    """Config stalker\n"""

    def __init__(self, bot) -> None:
        self.bot = bot

    async def get_tz(self, guild_id):
        guild = GuildData(self.bot.db)
        guild_data = await guild.get(multi=False, guild_id=guild_id)
        if not guild_data["timezone"]:
            return None
        else:
            return guild_data["timezone"]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def monitor(self, ctx, member: Member, channel: TextChannel):
        """Add a member as a monitor"""
        guild_timezone = await self.get_tz(ctx.guild.id)
        if not guild_timezone:
            return await ctx.send(
                f"Please set timezone using `{ctx.prefix}settz` command."
            )

        user = User(self.bot.db)
        log = Log(self.bot.db)

        monitor = await user.get(multi=False, guild_id=ctx.guild.id, user_id=member.id)
        if monitor:
            return await ctx.send(f"{member} has already been monitored.")

        await user.insert(
            mentor_id=ctx.author.id,
            guild_id=ctx.guild.id,
            user_id=member.id,
            channel_id=channel.id,
        )
        now = datetime.now(timezone(guild_timezone))

        await log.insert(
            status=member.status.name,
            user_id=member.id,
            guild_id=ctx.guild.id,
            started=now,
        )

        self.bot.monitored_users.add(member.id)

        await ctx.send(f"{member} will get monitored from now.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, member: Member):
        """Remove a monitor"""
        user = User(self.bot.db)
        log = Log(self.bot.db)
        monitor = await user.get(multi=False, guild_id=ctx.guild.id, user_id=member.id)
        if not monitor:
            return await ctx.send("This member is not monitored.")

        await user.delete(id=monitor["id"])
        await log.delete(user_id=member.id, guild_id=ctx.guild.id)

        try:
            self.bot.monitored_users.add(member.id)
        except KeyError:
            pass

        await ctx.send("Monitor deleted.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def update(self, ctx, member: Member, channel: TextChannel):
        """Change/Update channel of a monitor"""
        user = User(self.bot.db)
        monitor = await user.get(multi=False, guild_id=ctx.guild.id, user_id=member.id)
        if not monitor:
            return await ctx.send("This member is not monitored.")

        await user.update({"id": monitor["id"]}, channel_id=channel.id)
        await ctx.send("Monitor has been updated.")


def setup(bot):
    bot.add_cog(Config(bot))
