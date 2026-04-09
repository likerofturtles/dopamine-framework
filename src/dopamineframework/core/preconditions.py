import discord
from discord import app_commands
from discord.ext import commands
from .errors import MissingDopaminePermissions, RateLimited, PreconditionFailed

def global_cooldown():
    async def predicate(interaction: discord.Interaction) -> bool:
        bot = interaction.client

        if not hasattr(bot, 'global_cooldown_mapping'):
            return True

        bucket = bot.global_cooldown_mapping.get_bucket(interaction.message or interaction)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            raise RateLimited(retry_after)

        return True

    return app_commands.check(predicate)


def permissions_preset(preset_name: str):
    PRESETS = {
        "moderator": {"manage_messages": True, "kick_members": True, "ban_members": True},
        "admin": {"administrator": True},
        "giveaways": {"manage_guild": True, "manage_messages": True},
        "automation": {"manage_guild": True, "manage_messages": True, "manage_channels": True},
        "manager": {"manage_guild": True, "manage_roles": True, "manage_channels": True},
        "support": {"manage_messages": True, "read_message_history": True},
        "security": {"view_audit_log": True, "moderate_members": True},
        "community": {"manage_expressions": True, "manage_threads": True, "create_public_threads": True},
        "technical": {"manage_webhooks": True, "manage_guild": True}
    }

    async def predicate(interaction: discord.Interaction) -> bool:
        bot = interaction.client

        if preset_name.lower() == "bot_owner":
            is_owner = (
                interaction.user.id in bot.owner_ids
                if bot.owner_ids else
                interaction.user.id == bot.owner_id
            )
            if not is_owner:
                raise PreconditionFailed("This command is restricted to the bot owner.")
            return True

        perms_to_check = PRESETS.get(preset_name.lower())
        if perms_to_check is None:
            raise ValueError(f"Dopamine Framework: Permission preset '{preset_name}' not found.")

        if not interaction.guild:
            raise PreconditionFailed("This command can only be used in a server.")

        permissions = interaction.permissions

        missing = [
            perm for perm, required in perms_to_check.items()
            if required and not getattr(permissions, perm)
        ]

        if missing:
            raise MissingDopaminePermissions(missing)

        return True

    return app_commands.check(predicate)

def has_permissions(**perms):

    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            raise PreconditionFailed("This command can only be used in a server.")

        permissions = interaction.permissions
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]

        if missing:
            raise MissingDopaminePermissions(missing)

        return True

    return app_commands.check(predicate)


def has_permissions_any(**perms):

    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            raise PreconditionFailed("This command can only be used in a server.")

        permissions = interaction.permissions

        has_at_least_one = any(
            getattr(permissions, perm) == value
            for perm, value in perms.items()
        )

        if not has_at_least_one:
            raise MissingDopaminePermissions(list(perms.keys()))

        return True

    return app_commands.check(predicate)

def cooldown(rate: int = 10, per: float = 60):
    mapping = commands.CooldownMapping.from_cooldown(rate, per, commands.BucketType.user)

    async def predicate(interaction: discord.Interaction) -> bool:
        bucket = mapping.get_bucket(interaction.message or interaction)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            raise RateLimited(retry_after)

        return True

    return app_commands.check(predicate)