import discord
import aiohttp
import os
import json
from redbot.core import commands
from pathlib import Path

class AICommand(commands.Cog, name="AICommand"):
    """
    Communicate with Shibebot AI for the Thunderdoge Gaming Community.
    """

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.ai_url = os.getenv("AI_ENDPOINT_URL", "http://placeholder.ai:5001/v1/chat/completions")
        self.system_prompt = os.getenv("AI_SYSTEM_PROMPT", "You are Shibebot, an AI made for the Thunderdoge gaming community. Keep responses short and funny.")
        self.chat_history_dir = Path("./chat_histories")
        self.chat_history_dir.mkdir(exist_ok=True)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    def get_user_chat_history_file_path(self, user_id: int) -> Path:
        return self.chat_history_dir / f"{user_id}.json"

    def update_chat_history(self, user_id: int, user_message: str, ai_response: str):
        file_path = self.get_user_chat_history_file_path(user_id)
        if file_path.exists():
            with open(file_path, "r") as file:
                history = json.load(file)
        else:
            history = {"messages": []}

        # Update history with user message and AI response
        history["messages"].append({"role": "user", "content": user_message})
        history["messages"].append({"role": "assistant", "content": ai_response})  
        history["messages"] = history["messages"][-50:]  # Keep only the last 50 messages

        with open(file_path, "w") as file:
            json.dump(history, file)

    async def fetch_ai_response(self, user_id: int, user_content: str):
        history_file_path = self.get_user_chat_history_file_path(user_id)
        if history_file_path.exists():
            with open(history_file_path, "r") as file:
                history = json.load(file)
        else:
            history = {"messages": [{"role": "system", "content": self.system_prompt}]}

        payload = {
            "messages": history["messages"] + [{"role": "user", "content": user_content}],
            "temperature": 0.7,
            "max_tokens": 150,
            "stream": False
        }

        async with self.session.post(self.ai_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                ai_response = data.get('choices', [{}])[0].get('message', {}).get('content', 'Error: Could not parse AI response.')
                self.update_chat_history(user_id, user_content, ai_response)  # Update history with AI response
                return ai_response
            else:
                return 'Error: Failed to fetch response from AI.'

    @commands.command(name="ai")
    async def ai_command(self, ctx, *, user_content: str):
        """
        Ask Shibebot anything!
        """
        await ctx.trigger_typing()
        try:
            ai_response = await self.fetch_ai_response(ctx.author.id, user_content)
            await ctx.send(ai_response)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    @commands.command(name="sai")
    async def stealth_ai_command(self, ctx, *, user_content: str):
        """
        Stealthily ask Shibebot anything!
        """
        await ctx.message.delete()
        await ctx.trigger_typing()
        try:
            ai_response = await self.fetch_ai_response(ctx.author.id, user_content)
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
