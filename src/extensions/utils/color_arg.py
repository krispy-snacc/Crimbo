from typing import Annotated
from discord import app_commands
from . import _colors as cl

color_db_path = "assets/colornames.json"
cl.load_colors(filepath=color_db_path)

class ColorInput:
    description = "Color name, hex code, or 'random'"
    def __init__(self, input: str):
        self.value = cl.parse_color_from_str(input)

class ColorInputTransformer(app_commands.Transformer):
    async def transform(self, interaction, value: str) -> ColorInput:
        return ColorInput(value)

ColorArg = app_commands.Transform[ColorInput, ColorInputTransformer]