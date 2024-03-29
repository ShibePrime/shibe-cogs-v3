from .ai import AICommand

def setup(bot):
    bot.add_cog(AICommand(bot))
