import discord
from discord.app_commands import AppCommandError

class PreconditionFailed(AppCommandError):
    pass

class MissingDopaminePermissions(PreconditionFailed):
    def __init__(self, missing_permissions: list[str]):
        self.missing_permissions = missing_permissions
        formatted = [perm.replace('_', ' ').title() for perm in missing_permissions]
        self.message = f"You can't use this command because you don't have the following permissions: **{', '.join(formatted)}**"
        super().__init__(self.message)

class RateLimited(PreconditionFailed):
    def __init__(self, retry_after: float):
        self.retry_after = retry_after
        self.message = f"You are using commands too quickly! Please try again in **{retry_after:.1f}s**."
        super().__init__(self.message)