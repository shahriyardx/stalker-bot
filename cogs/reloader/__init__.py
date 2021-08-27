import os
import inspect
from discord.ext import commands, tasks


class Reloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reloader.start()

    @tasks.loop(seconds=3)
    async def reloader(self):
        extensions = self.bot.extensions.copy()

        for extension, path in extensions.items():
            path = inspect.getfile(path)
            time = os.path.getmtime(path)

            try:
                if self.last_modified_time[extension] == time:
                    continue
            except KeyError:
                self.last_modified_time[extension] = time

            try:
                self.bot.reload_extension(extension)
            except commands.ExtensionError:
                print(f"❌ Couldn't reload extension: {extension}")
            except commands.ExtensionNotLoaded:
                continue
            else:
                print(f"✔️  Reloaded extension: {extension}")
            finally:
                self.last_modified_time[extension] = time

    @reloader.before_loop
    async def cache_modified_times(self):
        self.last_modified_time = {}
        extensions = self.bot.extensions.copy()

        for extension, path in extensions.items():
            path = inspect.getfile(path)
            time = os.path.getmtime(path)
            self.last_modified_time[extension] = time

    def cog_unload(self):
        self.reloader.stop()


def setup(bot):
    bot.add_cog(Reloader(bot))
