## `bot.py` Documentation


This is the entry point for the framework. Follow the initialization example below to load your Discord bot with Dopamine Framework (Note: For simplicity and security's sake, the framework does NOT run/start the bot automatically. You have to do it yourself, as shown in the code snippet below).

---

### Initialization (in your main.py)

```python
from dopamineframework import Bot
import discord

bot = Bot(
    command_prefix="!",
    cogs_path="cogs",
    log_path="data/logs.db",
    default_diagnostics=True,
    status=discord.Status.online,
    activity=discord.Game(name="Example"),
    intents=discord.Intents.default()
)

bot.run("YOUR_TOKEN_HERE")

```

#### Parameters

| Parameter           | Type | Default   | Description |
|---------------------| --- |-----------| --- |
| `command_prefix`    | `str` | `!`       | Prefix for text-based commands. |
| `cogs_path`         | `str` | `"cogs"`  | Directory containing `.py` files to be loaded as extensions. |
| `log_path`          | `str` | `None`    | File path for the `aiosqlite` logging database. If `None`, the Logging Manager is disabled. |
| `default_diagnostics` | `bool` | `True`    | Whether to load the built-in diagnostics extension. |
| `status`            | `discord.Status` | `None`    | Initial presence status for the bot. |
| `activity`          | `discord.Activity` | `None`    | Initial activity for the bot. |
| `*args / **kwargs`  | `Any` | -         | Supports all standard `discord.ext.commands.Bot` arguments (e.g., `intents`). |

---

### Usage Notes

* **IMPORTANT:** Do NOT define a `steup_hook` or `on_ready` function in your main.py. The framework already defines those. If you try to define your own, the bot may crash due to conficts.