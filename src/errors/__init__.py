import discord
from config import CONFIG

async def global_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if CONFIG.DEBUG:
        embed = discord.Embed(description=f'**{str(error)}**', color=CONFIG.PRIMARY_COLOR)
        await interaction.followup.send(embed=embed, ephemeral=True)
    print(error.with_traceback())
