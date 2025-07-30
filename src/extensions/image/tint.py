from __future__ import annotations

import discord
from discord import app_commands

from bot import Crimbo

from . import image_group
from . import _effect as ef
from extensions.utils.color_arg import ColorArg
import numpy as np

name: str = "tint"
description: str = "adds a tint effect to the image"

kernel_src = """
__constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP | CLK_FILTER_NEAREST;

__kernel void _main(
    read_only image2d_t src,
    write_only image2d_t dst,
    uchar tint_r,
    uchar tint_g,
    uchar tint_b,
    float strength
) {
    int2 pos = (int2)(get_global_id(0), get_global_id(1));
    uint4 pixel = read_imageui(src, sampler, pos);

    pixel.x = convert_uint(pixel.x * (1.0f - strength) + tint_r * strength);
    pixel.y = convert_uint(pixel.y * (1.0f - strength) + tint_g * strength);
    pixel.z = convert_uint(pixel.z * (1.0f - strength) + tint_b * strength);

    write_imageui(dst, pos, pixel);
}

"""

@image_group.command(name=name, description=description)
@app_commands.describe(image="The image to put this effect on")
@app_commands.describe(color="The color of the tint to be applied")
@app_commands.describe(intensity="Amount of intensity")
@app_commands.describe(ephemeral="Should the response be ephemeral (only visible to you)")
async def effect(
    interaction: discord.Interaction, 
    image: discord.Attachment, 
    color: ColorArg, 
    intensity: app_commands.Range[float, 0.0, 100.0], 
    ephemeral: bool=False
):
    """Adds a tint to the given image"""
    bot: Crimbo = interaction.client
    await interaction.response.defer()
    embed, file = ef.image_to_embed(
                ef.apply_effect(
                    kernel_src, 
                    await ef.attachment_to_image(image),
                    np.uint8(color.value.r * 255),
                    np.uint8(color.value.g * 255),
                    np.uint8(color.value.b * 255),
                    np.float32(min(max(intensity, 0), 100)/100)
                ),
                bot.config.primary_color
            )
    # embed, file = ef.image_to_embed(
    #             await ef.attachment_to_image(image),
    #             bot.config.primary_color
    #         )
    await interaction.followup.send(embed=embed, file=file, ephemeral=ephemeral)
