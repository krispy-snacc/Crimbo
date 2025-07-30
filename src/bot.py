from logger import log
import discord
from discord import app_commands
from discord.ext import commands

from config import CONFIG
import errors
from extensions.utils.gen_helpers import walk_all_commands

import tracemalloc
tracemalloc.start()

class Crimbo(commands.Bot):
    
    intents: discord.Intents = discord.Intents.none()
    
    def __init__(self, init_exts:list[str] = [], **kwargs):
        super().__init__(command_prefix=None, intents=self.intents, **kwargs)
        self._initial_extensions = init_exts

    async def setup_hook(self):
        
        self.tree.error(errors.global_app_command_error)
        for ext in self._initial_extensions:
            await self.load_extension(ext)

        # --- Sync Commands ---
        guilds = self.guilds
        for i, guild in enumerate(guilds):
            await self.tree.sync(guild=guild)
        await self.tree.sync()

        # --- Add IDs ---

        # Get global commands from Discord
        app_id = self.user.id
        raw_cmds = await self.http.get_global_commands(app_id)

        # Build a lookup from name to ID
        id_lookup = {}
        for raw in raw_cmds:
            name_parts = [raw["name"]]
            option = raw
            while option.get("options") and option["options"][0].get("type") == 1:  # type 1 = subcommand/subgroup
                option = option["options"][0]
                name_parts.append(option["name"])
            full_name = " ".join(name_parts)
            id_lookup[full_name] = int(raw["id"])

        # Attach IDs to local commands
        for full_path, cmd in walk_all_commands(self.tree.get_commands()):
            if full_path in id_lookup:
                cmd.extras["id"] = id_lookup[full_path]
            else:
                log.warning(f"⚠️ No ID found for /{full_path}")

    async def on_interaction(self, interaction: discord.Interaction):
        if not CONFIG.DEBUG: return
        if interaction.type == discord.InteractionType.application_command:
            cmd = interaction.command
            if cmd:
                qualified_name = getattr(cmd, "qualified_name", "<unknown>")
                log.debug(f"[CMD] {interaction.user} ran /{qualified_name}")

    async def on_ready(self):
        version = CONFIG.VERSION
        version_name = f"v{version}" if version else f"unknown"
        if CONFIG.DEBUG: log.debug(f"{self.user.name} ({version_name}) is now ready!")
    

