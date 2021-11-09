import discord
from discord_slash import SlashContext


async def basicerror(ctx: SlashContext):
    embed = discord.Embed(title="Error:warning:", colour=discord.Colour.red())
    embed.add_field(name="Something went wrong!", value="Please Contact antonstech#9729")
    embed.set_footer(text="Or look for Help on discord.gg/bHQGfxFzhQ  :)")
    await ctx.channel.send(embed=embed)