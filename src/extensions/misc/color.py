from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo
from . import misc_group
from utils import _colors as cl


async def color_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    suggested_colors = cl.get_color_suggestion(current) 
    return [
        app_commands.Choice(name=color, value=color)
        for color in suggested_colors
    ][:10]


name: str = "color"
description: str = "describes a color"

color_db_path = "assets/colornames.json"
cl.load_colors(filepath=color_db_path)

@misc_group.command(name=name, description=description)
@app_commands.describe(color="The color to get the info about")
@app_commands.describe(ephemeral="Should the response be ephemeral (only visible to you)")
@app_commands.autocomplete(color=color_autocomplete)
async def color(interaction: discord.Interaction, color: str="random", ephemeral: bool=False):
    """Gives detailed info about a color thats provided
    Color must be in either hex format `#808080` or color name from suggestions"""
    await interaction.response.defer()
    embed = cl.get_color_embed(color)
    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
