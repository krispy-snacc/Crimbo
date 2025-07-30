import discord

async def global_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    embed = discord.Embed(description=f'**{str(error)}**', color=interaction.client.config.primary_color)
    await interaction.followup.send(embed=embed, ephemeral=True)
    print(error.with_traceback())
