from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo

class HelloCog(commands.Cog):
    name: str = "hello"
    description: str = "A hello Command to say hello"

    def __init__(self, bot: Crimbo):
        self.bot: Crimbo = bot

    @app_commands.command(name=name, description=description)
    @app_commands.describe(ephemeral="Should the response be ephemeral (only visible to you)")
    async def hello(self, interaction: discord.Interaction, ephemeral: bool=False):
        """A nice little hello command"""
        await interaction.response.send_message("Hello there!", ephemeral=ephemeral)

async def setup(bot: Crimbo):
    await bot.add_cog(HelloCog(bot))