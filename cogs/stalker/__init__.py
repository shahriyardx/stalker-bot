import discord
from pytz import timezone
from datetime import datetime
from discord.ext import commands
from humanize import precisedelta
from database import User, Log, GuildData


class Stalker(commands.Cog):
    """The stalker cog"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.status == after.status or after.id not in self.bot.monitored_users:
            return

        user = User(self.bot.db)
        log = Log(self.bot.db)
        guild = GuildData(self.bot.db)

        target = await user.get(
            multi=False, user_id=before.id, guild_id=before.guild.id
        )

        guild_data = await guild.get(multi=False, guild_id=before.guild.id)
        if not target:
            return

        last_log = await log.get_last_log(user_id=before.id, guild_id=before.guild.id)
        now = datetime.now(timezone(guild_data["timezone"]))
        if last_log:
            await log.update({"id": last_log["id"]}, ended=now)

        await log.insert(
            user_id=before.id,
            guild_id=before.guild.id,
            status=after.status.name,
            started=now,
            ended=None,
        )

        delta = now - last_log["started"]
        delta_str = precisedelta(delta, format="%0.0f")

        channel = before.guild.get_channel(target["channel_id"])
        if channel:
            embed = discord.Embed(title=f"Status update [{after}]")
            embed.description = ""
            embed.description += f"**Current Status** : {after.status.name.title()} {self.bot.status_emojis[after.status.name]} \n"
            embed.description += f"**Previous Status** : {before.status.name.title()} {self.bot.status_emojis[before.status.name]} \n\n"

            colors = {
                "online": 0x57F287,
                "offline": 0xFFFFFC,
                "dnd": 0xED4245,
                "idle": 0xFEE75C,
            }
            embed.description += f"Was **{before.status.name}** for : {delta_str}"
            embed.color = colors[after.status.name]
            embed.set_thumbnail(url=after.avatar_url)

            try:
                await channel.send(embed=embed)
            except:
                pass


def setup(bot):
    bot.add_cog(Stalker(bot))
