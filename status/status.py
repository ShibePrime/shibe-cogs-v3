
import discord

from redbot.core import commands

BaseCog = getattr(commands, "Cog", object)

class status(BaseCog):
    """gib status pls"""

    @commands.command(pass_context=True)
    async def status(self, ctx, *, member: discord.Member = None):
        """gib status"""
        author = ctx.author
        guild = ctx.guild

        if not member:
            member = author

        for s in member.activities:
            if isinstance(s, discord.CustomActivity):
                status_string = s

        name = str(member)
        name = " ~ ".join((name, member.nick)) if member.nick else name
        data = discord.Embed(title = name + "'s status",description=status_string, colour=member.colour)
        embed.set_thumbnail(url = member.avatar_url_as(static_format="png"))

        await ctx.send(embed=data)
