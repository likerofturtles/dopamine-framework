## Dopamine Commands Documentation
<sub>(This documentation is about the framework's `@dopamine_commands` wrapper for standard discord.py's decorator `@app_commands`, and about how to use the preconditions feature through it. To read about the decorators meant to be used with slash commands when you use the discord.py `@app_commands.command` decorator instead of Dopamine Framework's equivalent, read `preconditions.md`.)

The `dopamine_commands` module provides a wrapper around standard `discord.py` app commands. It simplifies the process of creating slash commands by integrating **permission presets**, **cooldowns**, and **global rate limiting** directly into a single decorator or group class.

---

## `dopamine_commands.command`
This decorator replaces the standard `@app_commands.command()`. It allows you to define functional constraints (like permissions and rate limits) as keyword arguments.

### **Usage**
```python
from dopamineframework.core import dopamine_commands

@dopamine_commands.command(
    name="ban",
    description="Ban a user from the server",
    permissions_preset="moderator",
    global_cooldown=True
)
async def ban_member(interaction: discord.Interaction, member: discord.Member):
    await member.ban()
    await interaction.response.send_message(f"Banned {member}")
```

### **Parameters**
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | Function Name | The name of the slash command. |
| `description` | `str` | Docstring | The command description visible in Discord. |
| `permissions_preset`| `str` | `None` | Apply a pre-defined set of permissions (e.g., `"admin"`, `"moderator"`). |
| `cooldown` | `tuple[int, float]`| `None` | A custom cooldown for this specific command: `(rate, per_seconds)`. |
| `global_cooldown` | `bool` | `True` | If `True`, the command respects the bot's global rate limit defined in the `Bot` class. |

---

## `dopamine_commands.Group`
A subclass of `app_commands.Group` that allows you to apply permissions or cooldowns to an entire group of subcommands at once.

### **Usage**
```python
from dopamineframework.core import dopamine_commands

admin_commands = dopamine_commands.Group(name="admin", description="Admin commands", permissions_preset="admin")
@admin_commands.command(name="check", description="This command only works if you're an admin!")
async def admin_check(interaction: discord.Interaction):
    interaction.response.send_message(f"{interaction.user.mention} You're an admin!")
```

---

## Permission Presets

| Preset Name | Required Permissions |
| :--- | :--- |
| `"bot_owner"` | Restricts usage to the bot owner/team owners. |
| `"admin"` | Administrator |
| `"moderator"` | Manage Messages, Kick Members, Ban Members |
| `"manager"` | Manage Guild, Roles, and Channels |
| `"support"` | Manage Messages, Read Message History |
| `"technical"` | Manage Webhooks, Manage Guild |
| `"giveaways"` | Manage Guild, Manage Messages |

---

## Error Handling
The framework includes a built-in error handler in `bot.py` that catches issues raised by these decorators.

* **Missing Permissions:** If a user lacks the required preset permissions, they receive a message listing the specific missing requirements (e.g., **"You can't use this command because you don't have the following permissions: Manage Messages"**).
* **Rate Limiting:** If a user triggers a local or global cooldown, they are notified of the exact time remaining: **"You are using commands too quickly! Please try again in 5.2s."**

---

## Key Differences from Standard Discord.py
1.  **Implicit Global Cooldown:** Every `dopamine_command` is protected by the global rate limit by default.
2. **Error Handling:** Precondition failures (cooldowns/perms) are automatically sent as ephemeral messages so they don't clutter the chat.