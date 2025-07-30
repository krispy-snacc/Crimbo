# Crimbo Discord Bot

Crimbo is a custom general purpose Discord bot built I'm working on, built with [discord.py](https://discordpy.readthedocs.io/) as a personal project to brush up on my discord bot coding skills after a long while since I made my last bot, now with slash commands and rich interaction based ui and designed for easy extension and customization. Planning to add more commands whenever I can get free time.

## Features

-   **Modular Extensions:** Easily add new commands via the `src/extensions/` directory.
-   **Command Groups:** Includes groups like `misc`, `image`, and root commands (`hello`, `ping`, `help`).
-   **Autocomplete Help:** Interactive help command with fuzzy search and autocomplete.
-   **Image Effects:** Apply effects such as tinting to images.
-   **Logging:** Color-coded logging for easier debugging.
-   **Docker Support:** Ready-to-deploy with Docker and docker-compose.

## Directory Structure

```
src/
  main.py           # Entry point
  bot.py            # Bot class and event handlers
  config.py         # Configuration management
  logger.py         # Logging setup
  extensions/
    hello.py        # Hello command
    ping.py         # Ping command
    help.py         # Help command with autocomplete
    image/          # Image effect commands
    misc/           # Miscellaneous commands
    utils/          # Utility functions
data/
  config.json       # Bot configuration
assets/
  colornames.json   # Color name data
```

## Getting Started

1. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Configure your bot:**

    - Edit `data/config.json` and `.env` with your Discord bot token and settings.

3. **Run the bot:**

    ```sh
    python src/main.py
    ```

4. **Docker (optional):**
    ```sh
    docker-compose up --build
    ```

## Usage

-   `/hello` — Greets the user.
-   `/ping` — Checks bot latency.
-   `/help` — Lists commands and provides info with autocomplete.
-   `/image tint` — Applies a tint effect to an image.
-   `/misc color` — Miscellaneous color-related commands.

**(these are all the commands right now, planning to add more in the future)**

## License

MIT
