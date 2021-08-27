from pytz import timezone
from discord.ext import commands
from database import GuildData
from datetime import datetime
from timetils import Formatter


class Settings(commands.Cog):
    """Settings commands"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str):
        """Set a new prefix"""
        guild = GuildData(self.bot.db)

        if len(new_prefix) > 20:
            return await ctx.send("Prefix can't be greater than 20 characters.")

        await guild.update({"guild_id": ctx.guild.id}, prefix=new_prefix)
        await ctx.send(f"Prefix has been changed to `{new_prefix}`.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settz(self, ctx, tz: str):
        """Set a timezone for this server."""
        guild = GuildData(self.bot.db)
        try:
            now = datetime.now(timezone(tz))
        except:
            return await ctx.send(
                "Invalid timezone. Use a valid timezone, e.g `Asia/Dhaka`. \nSearch for your timezone <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>"
            )

        await guild.update({"guild_id": ctx.guild.id}, timezone=tz)
        time = Formatter().natural_datetime(now)

        return await ctx.send(f"Timezone updated and current time is `{time}`")


def setup(bot):
    bot.add_cog(Settings(bot))
