from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo


class MiscGroup(app_commands.Group):
    name: str = "miscelleneous"
    description: str = "Miscelleneous commands"
    emoji = u'ℹ️'

    def __init__(self):
        super().__init__(name=self.name, description=self.description)


misc_group = MiscGroup()

from . import (
    color
)

class MiscCog(commands.Cog):
    def __init__(self, bot: Crimbo):
        self.bot = bot


async def setup(bot: Crimbo):
    bot.tree.add_command(misc_group)
    await bot.add_cog(MiscCog(bot))