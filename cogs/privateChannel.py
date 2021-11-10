import ast

import discord
from discord.ext.commands import AutoShardedBot, Cog
from discord_slash import cog_ext, SlashContext
from discord.errors import NotFound

from utils import utils

utils.LOGGER.debug(f"Trying to connect to the database at {utils.CONFIG.DATABASE_HOST}")
# Connect do database
utils.LOGGER.debug(f"Successfully connected to {utils.CONFIG.DATABASE_HOST}")


class PrivateChannel(Cog):
    def __init(self, bot: AutoShardedBot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="private-channel", description="Allows you to create Private Channels :)", options=[
        {
            "name": "create",
            "description": "Create a private channel",
            "type": 3,
            "required": "false"
        },

        {
            "name": "delete",
            "description": "Delete your own private channel",
            "type": 3,
            "required": "false"
        },

        {
            "name": "allow",
            "description": "Allow a person to join your private channel",
            "type": 6,
            "required": "false"
        },

        {
            "name": "deny",
            "description": "Deny a person access to your private channel",
            "type": 6,
            "required": "false"
        },

        {
            "name": "remove",
            "description": "(ADMIN ONLY) remove a private channel",
            "type": 7,
            "required": "false"
        },

        {
            "name": "on-or-off",
            "description": "(ADMIN ONLY) lets you turn on or off the whole feature",
            "type": 3,
            "required": "false",
            "choices": [
                {
                    "name": "on",
                    "value": "on"
                },
                {
                    "name": "off",
                    "value": "off"
                }
            ]
        },

        {
            "name": "category",
            "description": "(ADMIN ONLY) lets you set the category where private channels should be created",
            "type": 7,
            "required": "false"
        }

    ])
    async def private_channel(self, ctx: SlashContext, **kwargs):
        await ctx.defer(hidden=True)

        feature_enabled: bool = False
        category_id: int = -1
        category: discord.CategoryChannel = None

        user_has_private_channel: bool = False
        user_private_channel_id: int = -1
        user_whitelisted_users: list = []

        cursor = utils.DB_CONNECTOR.get_new_cursor()

        guild_data_sql = "select category_id, is_enabled from private_channels_guild_data where guild_id = %s"
        cursor.execute(guild_data_sql, (ctx.guild.id,))

        guild_data = cursor.fetchone()

        if guild_data is not None:
            category_id, feature_enabled = guild_data

        if feature_enabled:
            user_data_sql = "select channel_id, whitelisted_users from private_channels where guild_id = %s and channel_owner_id = %s"
            cursor.execute(user_data_sql, (ctx.guild.id, ctx.author.id))
            category = discord.utils.get(ctx.guild.categories, id=category_id)

            user_data = cursor.fetchone()

            if user_data is not None:
                user_has_private_channel = True
                user_private_channel_id, whitelisted_users = user_data
                user_whitelisted_users = ast.literal_eval(whitelisted_users)

        # print(f"{feature_enabled=}, {category_id=}, {user_has_private_channel=}, {user_private_channel_id=}, {user_whitelisted_users=}")

        if "create" in kwargs:
            channel_name = kwargs["create"]

            if not feature_enabled:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "This feature isn't enabled yet. Contact one of your server admins!", discord.Color.red()), hidden=True)
                return

            if user_has_private_channel:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "You already have a private channel!", discord.Color.red()), hidden=True)
                return
            guild = ctx.guild
            channel_created = await category.create_voice_channel(channel_name, bitrate=guild.bitrate_limit,  overwrites={
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False),
                ctx.author: discord.PermissionOverwrite(connect=True, move_members=True, speak=True,
                                                  mute_members=True, use_voice_activation=True,
                                                  view_channel=True, stream=True)
            }, reason="Private-Channel got created")

            create_sql = "insert into private_channels (channel_owner_id, channel_id, whitelisted_users, guild_id) values (%s, %s, %s, %s)"
            cursor.execute(create_sql, (ctx.author.id, channel_created.id, "[]", ctx.guild.id))
            utils.DB_CONNECTOR.commit()
            await ctx.send(embed=utils.return_embed(ctx, "Private Channel", f"Private channel with the name \"{channel_name}\" got created: {channel_created.mention}", discord.Color.green()), hidden=True)

        elif "delete" in kwargs:
            if not feature_enabled:
                await ctx.send(embed=utils.return_embed(ctx, "Error",
                                                        "This feature isn't enabled yet. Contact one of your server admins!",
                                                        discord.Color.red()), hidden=True)
                return

            if not user_has_private_channel:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "You don't have a private channel!", discord.Color.red()), hidden=True)
                return

            private_channel: discord.VoiceChannel = discord.utils.get(ctx.guild.voice_channels, id=user_private_channel_id)

            if private_channel is None:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "Could not find private channel!", discord.Color.red()), hidden=True)
                return

            await private_channel.delete(reason="Private-Channel got deleted")

            delete_sql = "delete from private_channels where guild_id = %s and channel_owner_id = %s and channel_id = %s"
            cursor.execute(delete_sql, (ctx.guild.id, ctx.author.id, user_private_channel_id))
            utils.DB_CONNECTOR.commit()

            await ctx.send(embed=utils.return_embed(ctx, "Private Channel", "Private channel got deleted!", discord.Color.green()), hidden=True)

        elif "allow" in kwargs:
            member_to_allow: discord.Member = kwargs["allow"]

            if not feature_enabled:
                await ctx.send(embed=utils.return_embed(ctx, "Error",
                                                        "This feature isn't enabled yet. Contact one of your server admins!",
                                                        discord.Color.red()), hidden=True)
                return

            if not user_has_private_channel:
                await ctx.send(
                    embed=utils.return_embed(ctx, "Error", "You don't have a private channel!", discord.Color.red()),
                    hidden=True)
                return

            private_channel: discord.VoiceChannel = discord.utils.get(ctx.guild.voice_channels,
                                                                      id=user_private_channel_id)

            if private_channel is None:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "Could not find private channel!",
                                                        discord.Color.red()), hidden=True)
                return

            user_whitelisted_users.append(member_to_allow.id)

            await private_channel.set_permissions(member_to_allow, overwrite=discord.PermissionOverwrite(connect=True, speak=True, use_voice_activation=True,
                                          view_channel=True, stream=True))

            update_sql = "update private_channels set whitelisted_users = %s where guild_id = %s and channel_id = %s and channel_owner_id = %s"
            cursor.execute(update_sql, (str(user_whitelisted_users), ctx.guild.id, private_channel.id, ctx.author.id))
            utils.DB_CONNECTOR.commit()

            await ctx.send(embed=utils.return_embed(ctx, "Private Channel", f"Successfully allowed {member_to_allow.mention} to access the private channel!", discord.Color.green()), hidden=True)

        elif "deny" in kwargs:
            member_to_disallow: discord.Member = kwargs["deny"]

            if not feature_enabled:
                await ctx.send(embed=utils.return_embed(ctx, "Error",
                                                        "This feature isn't enabled yet. Contact one of your server admins!",
                                                        discord.Color.red()), hidden=True)
                return

            if not user_has_private_channel:
                await ctx.send(
                    embed=utils.return_embed(ctx, "Error", "You don't have a private channel!", discord.Color.red()),
                    hidden=True)
                return

            private_channel: discord.VoiceChannel = discord.utils.get(ctx.guild.voice_channels,
                                                                      id=user_private_channel_id)

            if private_channel is None:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "Could not find private channel!",
                                                        discord.Color.red()), hidden=True)
                return

            await private_channel.set_permissions(member_to_disallow, overwrite=discord.PermissionOverwrite(connect=False))

            if member_to_disallow in private_channel.members:
                # user is in private channel, he's getting kicked
                await member_to_disallow.move_to(channel=None, reason="User got denied access in a private channel!")

            if member_to_disallow.id in user_whitelisted_users:
                user_whitelisted_users.remove(member_to_disallow.id)
            else:
                utils.LOGGER.debug("Disallowed member not tracked...")

            update_sql = "update private_channels set whitelisted_users = %s where guild_id = %s and channel_id = %s and channel_owner_id = %s"
            cursor.execute(update_sql, (str(user_whitelisted_users), ctx.guild.id, private_channel.id, ctx.author.id))
            utils.DB_CONNECTOR.commit()

            await ctx.send(embed=utils.return_embed(ctx, "Private Channel", f"Successfully denied {member_to_disallow.mention} access to the private channel!", discord.Color.green()), hidden=True)

        elif "remove" in kwargs:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "Insufficient permissions!", discord.Color.red()), hidden=True)
                return

            channel_to_remove = kwargs["remove"]

            if not isinstance(channel_to_remove, discord.VoiceChannel):
                await ctx.send(embed=utils.return_embed(ctx, "Error", "You didn't select a voice channel!", discord.Color.red()), hidden=True)
                return

            get_channel_sql = "select * from private_channels where channel_id = %s and guild_id = %s"
            cursor.execute(get_channel_sql, (channel_to_remove.id, ctx.guild.id))

            result = cursor.fetchone()

            if result is None:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "That is not a private channel!", discord.Color.red()), hidden=True)
                return

            channel_owner_id, channel_id, whitelisted_users, guild_id = result

            if channel_to_remove is None:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "That private channel was not found!", discord.Color.red()), hidden=True)
                return

            await channel_to_remove.delete(reason="Administrator deleted this private-channel!")

            remove_channel_sql = "delete from private_channels where channel_id = %s and guild_id = %s and channel_id = %s"
            cursor.execute(remove_channel_sql, (channel_to_remove.id, ctx.guild.id, channel_id))
            utils.DB_CONNECTOR.commit()

            owner_of_private_channel = await ctx.guild.fetch_member(channel_owner_id)

            await ctx.send(embed=utils.return_embed(ctx, "Private Channel", f"The private channel {'from ' + owner_of_private_channel.mention if owner_of_private_channel is not None else ''} got deleted!", discord.Color.green()), hidden=True)

        elif "on-or-off" in kwargs:
            value = kwargs["on-or-off"]

            if value == "on":
                check_sql = "select * from private_channels_guild_data where guild_id = %s"
                cursor.execute(check_sql, (ctx.guild.id,))

                if cursor.fetchone() is None:
                    # we don't have any entries aka this is a "clean" server

                    created_category = await ctx.guild.create_category("Private-Channels")

                    create_sql = "insert into private_channels_guild_data (guild_id, category_id, is_enabled) values (%s, %s, %s)"
                    cursor.execute(create_sql, (ctx.guild.id, created_category.id, True))
                    utils.DB_CONNECTOR.commit()

                else:
                    category = discord.utils.get(ctx.guild.categories, id=category_id)
                    category = category if category is not None else await ctx.guild.create_category("Private-Channels")
                    utils.LOGGER.debug("Created new private-channel since the old one wasn't found")

                    update_sql = "update private_channels_guild_data set is_enabled = %s, category_id = %s where guild_id = %s"
                    cursor.execute(update_sql, (True, category.id, ctx.guild.id))
                    utils.DB_CONNECTOR.commit()

                await ctx.send(embed=utils.return_embed(ctx, "Private Channels", "Private channels have been enabled!", discord.Color.green()), hidden=True)

            else:
                del_sql = "update private_channels_guild_data set is_enabled = %s where guild_id = %s"
                cursor.execute(del_sql, (False, ctx.guild.id))
                utils.DB_CONNECTOR.commit()

                await ctx.send(embed=utils.return_embed(ctx, "Private Channels", "Private channels have been disabled!", discord.Color.green()), hidden=True)

        elif "category" in kwargs:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send(embed=utils.return_embed(ctx, "Error", "Insufficient permissions!", discord.Color.red()),
                               hidden=True)
                return

            new_category = kwargs["category"]

            if not isinstance(new_category, discord.CategoryChannel):
                await ctx.send(embed=utils.return_embed(ctx, "Error", "You didn't select a category!", discord.Color.red()), hidden=True)
                return

            check_sql = "select * from private_channels_guild_data where guild_id = %s"
            cursor.execute(check_sql, (ctx.guild.id,))

            if cursor.fetchone() is None:
                # we don't have any entries aka this is a "clean" server

                create_sql = "insert into private_channels_guild_data (guild_id, category_id, is_enabled) values (%s, %s, %s)"
                cursor.execute(create_sql, (ctx.guild.id, new_category.id, False))
                utils.DB_CONNECTOR.commit()

            else:
                update_sql = "update private_channels_guild_data set category_id = %s where guild_id = %s"
                cursor.execute(update_sql, (new_category.id, ctx.guild.id))
                utils.DB_CONNECTOR.commit()

            await ctx.send(embed=utils.return_embed(ctx, "Private Channels", f"All future private channels will now be created in {new_category.mention}!", discord.Color.green()), hidden=True)

        else:
            await ctx.send("Invalid Option", hidden=True)


def setup(bot: AutoShardedBot):
    bot.add_cog(PrivateChannel(bot))
