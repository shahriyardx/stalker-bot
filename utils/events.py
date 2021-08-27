from discord.ext import commands
from database import Log, User


class Events(commands.Cog):
    """Events cog"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log = Log(self.bot.db)
        user = User(self.bot.db)

        await user.delete(user_id=member.id, guild_id=member.guild.id)
        await log.delete(user_id=member.id, guild_id=member.guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
