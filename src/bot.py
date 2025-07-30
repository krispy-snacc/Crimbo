import discord
from discord import app_commands
from discord.ext import commands
import sys
import tracemalloc

import config
import errors

tracemalloc.start()

from typing import Iterable, Generator

def walk_all_commands(
    commands: Iterable[app_commands.Command | app_commands.Group],
    parent: str = ""
) -> Generator[tuple[str, app_commands.Command], None, None]:
    for cmd in commands:
        full_name = f"{parent} {cmd.name}".strip()
        if isinstance(cmd, app_commands.Group):
            yield from walk_all_commands(cmd.commands, full_name)
        else:
            yield (full_name, cmd)


class Crimbo(commands.Bot):
    
    intents: discord.Intents = discord.Intents.none()
    
    def __init__(self, init_exts:list[str] = [], **kwargs):
        super().__init__(command_prefix=None, intents=self.intents, **kwargs)
        self._initial_extensions = init_exts
        self.config: dict = config.CONFIG
        self.config.primary_color = discord.Color.from_str(self.config.primary_color or "#f5ad42")

    async def setup_hook(self):
        
        self.tree.error(errors.global_app_command_error)
        for ext in self._initial_extensions:
            await self.load_extension(ext)

        # --- Sync Commands ---
        guilds = self.guilds
        for i, guild in enumerate(guilds):
            sys.stdout.write(f"\rSyncing Guilds: {i+1}/{len(guilds)}")
            sys.stdout.flush()
            print()
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
                print(f"Attached ID to /{full_path}: {cmd.extras['id']}")
            else:
                print(f"⚠️ No ID found for /{full_path}")

    async def on_ready(self):
        version = self.config.get("version")
        version_name = f"v{version}" if version else f"unknown"
        print(f"{self.user.name} ({version_name}) is now ready!")

