from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo


class PingCog(commands.Cog):
    name: str = "ping"
    description: str = "Checks the latency of the bot"

    def __init__(self, bot: Crimbo):
        self.bot: Crimbo = bot

    @app_commands.command(name=name, description=description)
    @app_commands.describe(ephemeral="Should the response be ephemeral (only visible to you)")
    async def ping(self, interaction: discord.Interaction, ephemeral: bool=False):
        """Gives information about the bot's latency (in ms)"""
        ping_latency = round(self.bot.latency * 1000)
        embed = discord.Embed(color=self.bot.config.primary_color)
        embed.add_field(name=':ping_pong: Ping Pong!', value=f"**{ping_latency} ms**")
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

async def setup(bot: Crimbo):
    await bot.add_cog(PingCog(bot))