from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo


class ImageGroup(app_commands.Group):
    name: str = "image"
    description: str = "image commands"
    emoji = u'📷'

    def __init__(self):
        super().__init__(name=self.name, description=self.description)


image_group = ImageGroup()

from . import (
    tint
)

class ImageCog(commands.Cog):
    def __init__(self, bot: Crimbo):
        self.bot = bot

async def setup(bot: Crimbo):
    bot.tree.add_command(image_group)
    await bot.add_cog(ImageCog(bot))