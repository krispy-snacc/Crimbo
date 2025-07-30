import random
import re
import json
import numpy as np
from colorzero import Color
from colorzero.types import RGB
from functools import lru_cache
import discord

loaded_colors: list[tuple[str, RGB]] = []

@lru_cache(maxsize=100)
def get_color_embed(color_str: str) -> discord.Embed:
    c = parse_color_from_str(color_str)

    data = {
        "name": find_closest_color_fast(c),
        "hex": col_to_hex(c),
        "rgb": col_to_rgb(c),
        "hsl": col_to_hsl(c),
        "image": f"https://api.alexflipnote.dev/colour/image/{col_to_hex(c).lstrip("#")}"
    }    

    embed = discord.Embed(color=discord.Color.from_str(data["hex"]))
    embed.add_field(name="Hex", value=data["hex"])
    embed.add_field(name="RGB", value=data["rgb"], inline=False)
    embed.add_field(name="HSL", value=data["hsl"], inline=False)
    embed.add_field(name="Name", value=find_closest_color_fast(c), inline=False)
    embed.set_thumbnail(url=data["image"])
    return embed

def parse_color_from_str(color_str: str) -> Color:
    c: Color = None
    if color_str.lower() == "random":
        c = random_color()
    else:
        if (re.match("^#?(?:[0-9a-fA-F]{3}){2}$", color_str)): 
            c = Color.from_string("#" + color_str.lower().lstrip('#'))
        else:
            found_color = get_color_from_name(color_str)
            if (found_color != None):
                c = found_color
            else:
                raise ValueError("invalid color pattern")
    
    return c

def get_color_from_name(color_str: str) -> tuple[str, RGB]:
    for c in loaded_colors:
        if color_str.lower() == c[0].lower(): return Color.from_rgb(*c[1])
    return None

@lru_cache(maxsize=100)
def get_color_suggestion(current: str) -> list[str]:
    return [color[0] for color in loaded_colors if current.lower() in color[0].lower()]

def random_color() -> discord.Color:
    return Color.from_rgb(*[random.random() for _ in range(3)])

def col_to_hex(c: Color):
    r, g, b = [round(x * 255) for x in c.rgb]
    return f"#{r:0>2x}{g:0>2x}{b:0>2x}"

def col_to_hsl(c: Color):
    h, l, s = c.hls
    return f"hsl({round(h * 360)}, {round(s * 100)}%, {round(l * 100)}%)"

def col_to_rgb(c: Color):
    r, g, b = [round(x * 255) for x in c.rgb]
    return f"rgb({r}, {g}, {b})"

def color_distance(rgb1: Color, rgb2: Color):
    return sum((a - b) ** 2 for a, b in zip(rgb1.rgb, rgb2.rgb))

def find_closest_color_fast(input_col: Color,):
    input_rgb = np.array(list(input_col.rgb))
    names = [name for name, _ in loaded_colors]
    rgb_values = np.array([rgb for _, rgb in loaded_colors])

    distances = np.sum((rgb_values - input_rgb) ** 2, axis=1)
    idx = np.argmin(distances)
    return names[idx]


def load_colors(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_colors = json.load(f)
    
    globals()["loaded_colors"] = [
        (str(color["name"]), Color.from_string(color["hex"]).rgb)
        for color in raw_colors
    ]

