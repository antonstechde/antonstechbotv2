import discord
from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext
from discord.channel import TextChannel
from discord.emoji import Emoji
from discord.role import Role
from discord.ext import commands
from discord.errors import Forbidden, NotFound

from utils import utils


class RoleReactions(Cog):
    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_subcommand(base="role_reaction", name="create", description="Create a role reaction")
    @commands.has_permissions(administrator=True)
    async def role_reactions_create(self, ctx: SlashContext, channel: TextChannel, message: str, emoji: Emoji, role: Role):
        await ctx.defer(hidden=False)

        try:
            message = int(message)
        except ValueError:
            await ctx.send(embed=utils.return_embed(ctx, "Error", "The message id is not a number!", discord.Color.red()))
            return

        try:
            fetched_message: discord.Message = await channel.fetch_message(message)
        except NotFound:
            await ctx.send(embed=utils.return_embed(ctx, "Error", "The message was not found!", discord.Color.red()))
            return

        # if the reaction is already on the message, this will handle it

        try:
            fetched_message.reactions.index(emoji)
        except ValueError:
            await fetched_message.add_reaction(emoji)

        cursor = utils.DB_CONNECTOR.get_new_cursor()

        # checks if a db entry is present and deletes it to avoid double entries since we don't have a primary key here
        sql = "select role_id from role_reactions where channel_id = %s and message_id = %s and emoji_id = %s"
        cursor.execute(sql, (channel.id, fetched_message.id, emoji))

        role_id = cursor.fetchone()

        if role_id is not None:
            sql = "delete from role_reactions where channel_id = %s and message_id = %s and emoji_id = %s and role_id = %s"
            cursor.execute(sql, (channel.id, fetched_message.id, emoji, role_id))
            utils.DB_CONNECTOR.commit()

        sql = "insert into role_reactions (channel_id, message_id, emoji_id, role_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (channel.id, fetched_message.id, emoji, role.id))

        utils.DB_CONNECTOR.commit()
        cursor.close()

        await ctx.send(embed=utils.return_embed(ctx, "Done", f"Successfully set up a role reaction at [this message]({fetched_message.jump_url})!", discord.Color.green()))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # using raw payload because this event won't fire if the message that's being reacted on isn't in the cache

        message_id = payload.message_id
        channel_id = payload.channel_id
        member: discord.Member = payload.member
        emoji: discord.PartialEmoji = payload.emoji
        guild_id = payload.guild_id

        guild: discord.Guild = self.bot.get_guild(guild_id)

        if guild is None:
            return

        cursor = utils.DB_CONNECTOR.get_new_cursor()

        sql = "select role_id from role_reactions where channel_id = %s and message_id = %s and emoji_id = %s"
        cursor.execute(sql, (channel_id, message_id, emoji.name))

        role_id = cursor.fetchone()

        if role_id is None:
            # no entries found, shouldn't happen
            return

        role_id, = role_id

        role: Role = guild.get_role(role_id)

        try:
            await member.add_roles(role, reason="Role-Reaction")
        except Forbidden as e:
            utils.LOGGER.debug(f"Could not give \"{member.display_name}\" the role \"{role.name}\" because the bot doesn't have permissions")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        message_id = payload.message_id
        channel_id = payload.channel_id
        user_id = payload.user_id
        emoji: discord.PartialEmoji = payload.emoji
        guild_id = payload.guild_id

        guild: discord.Guild = self.bot.get_guild(guild_id)

        if guild is None:
            return

        member: discord.Member = await guild.fetch_member(user_id)

        if member is None:
            utils.LOGGER.debug("Could not find member, not continuing in role-removing")
            return

        cursor = utils.DB_CONNECTOR.get_new_cursor()

        sql = "select role_id from role_reactions where channel_id = %s and message_id = %s and emoji_id = %s"
        cursor.execute(sql, (channel_id, message_id, emoji.name))

        role_id = cursor.fetchone()

        if role_id is None:
            # no entries found
            return

        role_id, = role_id

        role: Role = guild.get_role(role_id)

        try:
            await member.remove_roles(role, reason="Role-Reaction")
        except Forbidden as e:
            utils.LOGGER.debug(
                f"Could not remove the role \"{role.name}\" from \"{member.display_name}\" because the bot doesn't have permissions")


def setup(bot: AutoShardedBot):
    bot.add_cog(RoleReactions(bot))
