# This init is required for each cog.
# Import your main class from the cog's folder.
from .status import status


def setup(bot):
    # Add the cog to the bot.
    bot.add_cog(status())
