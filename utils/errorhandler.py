from nextcord.ext import commands


class ErrorHandler(commands.Cog):
    """The error handler"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(
            error,
            (
                commands.BadArgument,
                commands.MissingRequiredArgument,
                commands.MemberNotFound,
            ),
        ):
            await ctx.send(f"{error}")

        elif isinstance(error, commands.NotOwner):
            pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
