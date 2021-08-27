from database import GuildData


async def get_prefix(bot, message):
    guild = GuildData(bot.db)

    guild_data = await guild.get_prefix(guild_id=message.guild.id)
    return guild_data["prefix"]
