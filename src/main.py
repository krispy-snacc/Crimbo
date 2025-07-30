import sys
from bot import Crimbo
from config import CONFIG

init_exts = [
    # root commands
    "extensions.hello",
    "extensions.ping",
    "extensions.help",

    # command groups
    "extensions.misc",

    # image groups
    "extensions.image",
]


if __name__ == "__main__":
    sys.stdout.write("\033c")
    sys.stdout.flush()
    bot = Crimbo(init_exts=init_exts)
    bot.run(CONFIG.TOKEN)