from bot import Crimbo

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
    bot = Crimbo(init_exts=init_exts)
    bot.run(bot.config["token"])