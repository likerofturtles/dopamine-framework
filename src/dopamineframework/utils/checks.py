import discord
from discord.ext import commands
from discord import app_commands

# MOD CHECKS (legacy and Next):
def prefix_mod_check():
    async def predicate(ctx):
        perms = ctx.author.guild_permissions
        if perms.moderate_members or perms.ban_members:
            return True
        raise commands.MissingPermissions(["moderate_members", "ban_members"])
    return commands.check(predicate)


async def mod_check(interaction: discord.Interaction):
    if not interaction.guild:
        raise app_commands.MissingPermissions(["moderate_members", "ban_members"])

    perms = interaction.user.guild_permissions
    if perms.moderate_members or perms.ban_members:
        return True
    raise app_commands.MissingPermissions(["moderate_members", "ban_members"])