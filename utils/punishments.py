import discord

# handle ban/kick/warn/mute commands


async def mute(ctx, user: discord.Member, length: int, mhd: str):
    ...


async def warn(ctx, user: discord.Member, reason: str):
    ...


async def kick(ctx, user: discord.Member, reason: str):
    await user.kick(reason=reason)
    await ctx.channel.send(f"Kicked {user.mention} with reason '{reason}'!")
    # use channel.send because .send was already used to respond to the slash command.

    # do some embed stuff?


async def ban(ctx, user: discord.Member, reason: str):
    await user.ban(reason=reason)
    await ctx.channel.send(f"Banned {user.mention} with reason '{reason}'!")
    # use channel.send because .send was already used to respond to the slash command.

    # do some embed stuff?
