from discord import app_commands
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

