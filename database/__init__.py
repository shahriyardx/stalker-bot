from .models import GuildData, User, Log


async def create_tables(db):
    await GuildData(db)._create()
    await User(db)._create()
    await Log(db)._create()
