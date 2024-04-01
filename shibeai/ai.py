import discord
import aiohttp
import os
from redbot.core import commands

class AICommand(commands.Cog, name="AICommand"):
    """
    Communicate with Shibebot AI for the Thunderdoge Gaming Community
    """

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        # Load settings from environment variables or use placeholders
        self.ai_url = os.getenv("AI_ENDPOINT_URL", "http://placeholder.ai:5001/v1/chat/completions")
        self.system_prompt = os.getenv("AI_SYSTEM_PROMPT", "You are Shibebot, an AI made for the Thunderdoge gaming community. Keep responses short and funny.")

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    async def fetch_ai_response(self, user_content: str):
        payload = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "max_tokens": 150,
            "stream": False
        }
        async with self.session.post(self.ai_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('choices', [{}])[0].get('message', {}).get('content', 'Error: Could not parse AI response.')
            else:
                return 'Error: Failed to fetch response from AI.'

    @commands.command(name="ai")
    async def ai_command(self, ctx, *, user_content: str):
        """
        Ask Shibebot anything!
        """
        await ctx.trigger_typing()
        try:
            ai_response = await self.fetch_ai_response(user_content)
            await ctx.send(ai_response)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    @commands.is_owner()
    @commands.command(name="aisetup")
    async def ai_setup(self, ctx, *, url: str):
        """
        Set the AI endpoint URL.
        """
        self.ai_url = url
        await ctx.send("AI endpoint URL has been updated.")

    @commands.is_owner()
    @commands.command(name="aisys")
    async def ai_sys(self, ctx, *, prompt: str):
        """
        Set the system prompt for the AI.
        """
        self.system_prompt = prompt
        await ctx.send("AI system prompt has been updated.")
