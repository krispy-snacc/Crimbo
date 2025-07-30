from __future__ import annotations
from typing import Iterable

import discord
from discord import app_commands
from discord.ext import commands
from bot import Crimbo
from config import CONFIG
from extensions.utils.gen_helpers import walk_all_commands
from extensions.utils.fuzzy_search import fuzzy_search_2


# TODO to implement
# gen_cmds = ['avatar', 'guildavatar', 'emote', 'help', 'ping', 'invite', 'prefix', 'roleinfo', 'serverinfo', 'userinfo', 'serverpfp', 'status', 'translate', 'yt', 'spoiler']
# fun_cmds = ['cat', 'choose', 'color', 'define', 'dog', 'fortune', 'pokemon', 'twitter', 'uwu', 'poll', 'getpoll', 'strawpoll', 'sub', 'sup', 'bannerize', 'rip', 'wallpaper', 'why', 'bored', 'wyr', 'topic', 'screenshot', 'lyrics', 'shower thought', 'movie', 'pet']
# img_cmds = ['captcha', 'colors', 'delete', 'vhs', 'wanted', 'wasted', 'chromatic', 'ree', 'boom', 'neon', 'photo', 'film', 'lego', 'edit (unstable)']


class Dropdown(discord.ui.Select):
    def __init__(self, bot: Crimbo, init_user_id: int):
        self.bot = bot
        self.init_user_id = init_user_id

        options = [
            discord.SelectOption(label=g.name.capitalize(), value=g.name, description=f"{g.name} Commands List", emoji=g.__getattribute__("emoji"))
            for g in self.bot.tree.get_commands()
            if isinstance(g, app_commands.Group)
        ]

        super().__init__(placeholder='Choose command category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.init_user_id:
            embed = await self.get_group_help_embed(self.values[0])
            await interaction.response.edit_message(embed = embed)

    async def get_group_help_embed(self, value: str) -> discord.Embed:
        group_cmd: app_commands.Group = next(
            iter(
                filter(lambda x: isinstance(x, app_commands.Group), self.bot.tree.get_commands())
                ), None)

        if not group_cmd: 
            raise ValueError(f"No group named {value}")
        
        gcs = [
            f"</{cmd.name}:{cmd.extras.get('id')}>"
            for cmd in group_cmd.commands
            if isinstance(cmd, app_commands.Command)
        ]
        embed = discord.Embed(title="Crimbo Help", description="```Use help <command> to get more info on a specific command```", color=CONFIG.PRIMARY_COLOR)
        embed.add_field(name=f"{value.capitalize()} Commands List", value=",\n".join(gcs))
        return embed

class DropdownView(discord.ui.View):
    def __init__(self, bot: Crimbo, init_user_id:int):
        super().__init__()
        self.value = None

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(bot, init_user_id))
        self.add_item(discord.ui.Button(label='Invite Crimbo!', url="https://google.com"))

def get_command_by_path(
    commands: Iterable[app_commands.Command, app_commands.Group],
    path: str
) -> app_commands.Command | None:
    parts = path.lstrip("/").strip().split()
    current_commands = commands
    cmd = None

    for part in parts:
        for c in current_commands:
            if c.name == part:
                cmd = c
                if isinstance(c, app_commands.Group):
                    current_commands = c.commands
                else:
                    current_commands = []
                break
        else:
            # Command part not found
            return None

    return cmd

class Help(commands.Cog):
    name: str = "help"
    description: str = "A help command to get info about other commands"

    def __init__(self, bot: Crimbo):
        self.bot: Crimbo = bot

    def get_commands(self, cmd_str:str, guild: int) -> list[str]:
        all_cmds = self.bot.tree.get_commands(guild=discord.Object(guild)) \
                    + self.bot.tree.get_commands()
        all_cmds = walk_all_commands(set(all_cmds))

        all_cmd_names = sorted([f"/{i[0]}" for i in all_cmds])
        if not cmd_str:
            return all_cmd_names[:15]
        
        cmd_results = sorted(fuzzy_search_2(cmd_str, all_cmd_names)[:15])
        return cmd_results 



    async def help_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=cmd_name, value=cmd_name)
            for cmd_name in self.get_commands(current, interaction.guild_id)
        ][:10]

    def get_command_from_name(
        self,
        command: str,
        guild: int
    ) -> app_commands.Command:
        all_cmds = self.bot.tree.get_commands(guild=discord.Object(guild)) \
                    + self.bot.tree.get_commands()
        all_cmds = set(all_cmds)
        cmd = get_command_by_path(all_cmds, command)
        return cmd



    @app_commands.command(name=name, description=description)
    @app_commands.describe(command="The command to get the info about")
    @app_commands.describe(ephemeral="Should the response be ephemeral (only visible to you)")
    @app_commands.autocomplete(command=help_autocomplete)
    async def help(self, interaction: discord.Interaction, command:str=None, ephemeral: bool=False):
        """Gives info about a given command"""
        if command != None:
            cmd = self.get_command_from_name(command, interaction.guild_id)
            if cmd != None:
                embed = discord.Embed(title=f"/{cmd.name}", description=cmd.description, color=CONFIG.PRIMARY_COLOR)
                doc = getattr(cmd.callback, "__doc__", None)
                if doc:
                    embed.add_field(name="Details", value=f"```{doc.strip()}```", inline=False)
                if cmd.extras.get("id", None): 
                    embed.add_field(name="Use", value=f"</{cmd.name}:{cmd.extras["id"]}>", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
            else:
                raise ValueError("Invalid Command")
        else:
            embed = discord.Embed(description='**Choose help category to learn more or use help <command> to know more about a specific command**', color=CONFIG.PRIMARY_COLOR)
            await interaction.response.send_message(embed=embed, view=DropdownView(bot=self.bot, init_user_id=interaction.user.id), ephemeral=ephemeral)

async def setup(bot: Crimbo):
    await bot.add_cog(Help(bot))
