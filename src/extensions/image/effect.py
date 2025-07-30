from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo
from . import image_group
from . import _effect

name: str = "effect"
description: str = "adds an effect to the image"

@image_group.command(name=name, description=description)
@app_commands.describe(image="The image to put the effect on")
@app_commands.describe(effect="The effect to put on the image")
@app_commands.choices(effect=[
    app_commands.Choice(name="tint", value="")
])
@app_commands.describe(ephemeral="Should the response be ephemeral (only visible to you)")
# @app_commands.autocomplete(color=color_autocomplete)
async def effect(interaction: discord.Interaction, image: discord.Attachment, ephemeral: bool=False):
    """"""
    await interaction.response.defer()
    embed = _effect.get_effect_image_embed(image, )
    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
