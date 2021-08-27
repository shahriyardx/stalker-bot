import os
from dotenv import load_dotenv
from asyncpg.pool import create_pool
from discord.ext import commands
from discord.flags import Intents
from config import extensions, db_config, mode
from database import create_tables
from database.helpers import get_prefix
from utils import fix_nulls, cache_emojis, cache_users


class StalkerBot(commands.Bot):
    """Stalker bot"""

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        self.db = await create_pool(**db_config)
        await create_tables(self.db)
        await fix_nulls(self)
        await cache_emojis(self)
        await cache_users(self)

        self.load_extension("jishaku")
        self.load_extension("dch")

        for extension in extensions:
            self.load_extension(extension)

        if mode == "development":
            self.load_extension("cogs.reloader")

        print(f"{self.user} is ready")

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)


intents = Intents.default()
intents.presences = True
intents.members = True

bot = StalkerBot(command_prefix=get_prefix, intents=intents)

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
