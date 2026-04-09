from discord import app_commands
from functools import wraps
from .preconditions import global_cooldown as g_cooldown, permissions_preset as preset, cooldown as local_cooldown


def command(
        name: str = None,
        description: str = None,
        global_cooldown: bool = True,
        permissions_preset: str = None,
        cooldown: tuple[int, float] = None,
        **kwargs
):
    def decorator(func):
        cmd = app_commands.command(
            name=name or func.__name__,
            description=description or (func.__doc__ or "No description provided"),
            **kwargs
        )(func)

        if permissions_preset:
            cmd = preset(permissions_preset)(cmd)

        if cooldown:
            rate, per = cooldown
            cmd = local_cooldown(rate, per)(cmd)
        elif global_cooldown:
            cmd = g_cooldown()(cmd)

        return cmd

    return decorator


class Group(app_commands.Group):
    def __init__(
            self,
            name: str = None,
            description: str = None,
            global_cooldown: bool = True,
            permissions_preset: str = None,
            cooldown: tuple[int, float] = None,
            **kwargs
    ):
        super().__init__(
            name=name or self.__class__.__name__.lower(),
            description=description or (self.__doc__ or "No description provided"),
            **kwargs
        )
        if permissions_preset:
            preset(permissions_preset)(self)

        if cooldown:
            rate, per = cooldown
            local_cooldown(rate, per)(self)
        elif global_cooldown:
            g_cooldown()(self)