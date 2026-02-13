

## `log.py` Documentation

The `LoggingManager` is accessible via `self.bot.logger` when a `logging_path` is provided during __bot initialization__ (read `DOCUMENTATION/bot.md` for more info about initialization).

---

### Core Methods

| Method | Signature | Description                                            |
| --- | --- |--------------------------------------------------------|
| **get** | `await get(guild_id: int)` | Returns the `channel_id` (int) or `None`.              |
| **set** | `await set(guild_id: int, channel_id: int)` | Set the channel for the logging channel for the guild. |
| **remove** | `await remove(guild_id: int)` | Deletes guild entry from DB and cache.                 |

---

### Implementation Patterns

#### Initialization

The manager is enabled by passing a valid database path to the `Bot` constructor.

```python
# Initialization (read DOCUMENTATION/bot.md for more info)
bot = Bot(
    ...,
    logging_path="databases/logs.db"
)
```

#### Fetching a Channel

`get()` returns an `int`, so you must fetch the channel object from `discord.py` to send messages.

```python
guild_id = 123456789
channel_id = await bot.logger.get(guild_id)

if channel_id:
    channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
    if channel:
        await channel.send("Log entry content.")
```

#### Setting/Updating a Channel

Used in configuration commands to map a specific channel for logging for a specific guild.

```python
@bot.tree.command(name="setlog")
async def set_log(interaction: discord.Interaction, channel: discord.TextChannel):
    await bot.logger.set(interaction.guild_id, channel.id)
    await interaction.response.send_message(f"Logs set to {channel.mention}")
```

---