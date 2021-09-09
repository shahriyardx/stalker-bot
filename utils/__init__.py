from database import GuildData, Log, User
from datetime import datetime
from pytz import timezone
from nextcord.utils import get


async def fix_nulls(bot):
    _log = Log(bot.db)
    _guild = GuildData(bot.db)

    all_logs = await _log.get_null_logs()

    for log in all_logs:
        guild = bot.get_guild(log["guild_id"])
        if guild:
            guild_data = await _guild.get(guild_id=guild.id)

            user = guild.get_member(log["user_id"])

            if user:
                status = user.status.name
                last_status = log["status"]

                if status != last_status:
                    now = datetime.now(timezone(guild_data["timezone"]))
                    await _log.update(
                        {"id": log["id"]},
                        ended=now,
                    )

                    await _log.insert(
                        status=user.status.name,
                        user_id=user.id,
                        guild_id=guild.id,
                        started=now,
                    )

            else:
                await _log.delete(id=log["id"])

        else:
            await _log.delete(guild_id=log["guild_id"])


async def cache_emojis(bot):
    support_guild = bot.get_guild(818926020585324555)
    emojis = {}

    emojis["online"] = get(support_guild.emojis, name="online")
    emojis["offline"] = get(support_guild.emojis, name="offline")
    emojis["idle"] = get(support_guild.emojis, name="idle")
    emojis["dnd"] = get(support_guild.emojis, name="dnd")

    bot.status_emojis = emojis


async def cache_users(bot):
    monitored_users = await User(bot.db).all()
    monitored_user_ids = {user["user_id"] for user in monitored_users}

    bot.monitored_users = monitored_user_ids
