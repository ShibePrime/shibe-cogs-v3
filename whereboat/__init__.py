from redbot.core.bot import Red
from .whereboat import whereboat


def setup(bot):
    # Add the cog to the bot.
    bot.add_cog(whereboat())
