import asyncio

import discord
from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext, ButtonStyle, ComponentContext
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import wait_for_component

from utils import utils


class ServerUtils(Cog):
    """
    This class is supposed to contain a lot of server based stuff like "channel create/delete" or "user punish/unpunish"
    """

    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    pun_opt = [
        {
            "name": "user",
            "description": "The user to punish",
            "required": True,
            "type": 6
        }
    ]

    @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="punish", description="punishes a user", options=pun_opt)
    async def _user_punish(self, ctx: SlashContext, user: discord.User):
        # add moderator permission restriction
        await ctx.defer(hidden=False)
        # This command is **not** hidden, so the user can see that he is being punished
        user_setbtn1 = [
            manage_components.create_button(
                label="BAN", style=ButtonStyle.red, custom_id="BAN"
            ),
            manage_components.create_button(
                label="KICK", style=ButtonStyle.red, custom_id="KICK"
            ),
        ]
        user_setbtn2 = [
            manage_components.create_button(
                label="WARN", style=ButtonStyle.blue, custom_id="WARN"
            ),
            manage_components.create_button(
                label="MUTE", style=ButtonStyle.blue, custom_id="MUTE"
            ),
        ]
        user_setbtn3 = [
            manage_components.create_button(
                label="Do nothing", style=ButtonStyle.gray, custom_id="nothing"
            )
        ]
        user_buttons_actionrow1 = manage_components.create_actionrow(*user_setbtn1)
        user_buttons_actionrow2 = manage_components.create_actionrow(*user_setbtn2)
        user_buttons_actionrow3 = manage_components.create_actionrow(*user_setbtn3)

        if (
                not ctx.author.guild_permissions.ban_members
                or not ctx.author.guild_permissions.kick_members
        ):
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"] = True
        if not ctx.author.guild_permissions.manage_messages:
            for i in range(2):
                user_buttons_actionrow2["components"][i]["disabled"] = True
        message = await ctx.send(
            f"What do you want to do with {user.mention}? (timeout: 60 seconds)",
            hidden=False,
            components=[
                user_buttons_actionrow1,
                user_buttons_actionrow2,
                user_buttons_actionrow3,
            ],
        )

        try:
            buttons: ComponentContext = await wait_for_component(self.bot, components=[user_buttons_actionrow1, user_buttons_actionrow2, user_buttons_actionrow3], timeout=60, check=lambda: ctx.author.id == buttons.author.id)
        except asyncio.TimeoutError:
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"]=True
                user_buttons_actionrow2["components"][i]["disabled"]=True
            user_buttons_actionrow2["components"][0]["disabled"]=True
            await message.edit(content="Timed out.", components=[user_buttons_actionrow1, user_buttons_actionrow2, user_buttons_actionrow3]) # Disable the Buttons
            return

        if buttons.component_id == "mute":
            ...  # do your own mute stuff here

        if buttons.component_id == "warn":
            ...  # do your own warn stuff here

        if buttons.component_id == "kick":
            # await user.kick(reason=
            ...  # do your own kick stuff with embeds or what you want



    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="un-punish", description="un-punishes a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="add-role", description="adds a role to a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="remove-role", description="removes a role from a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="create", description="creates a role")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="edit", description="edits a role")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="delete", description="deletes a role")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="create", description="creates a channel")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="edit", description="edits a channel") # not sure about that one
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="delete", description="deletes a channel")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="create", description="creates a category")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="edit", description="edits a category") # not sure about that one
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="delete", description="deletes a category")



def setup(bot: AutoShardedBot):
    bot.add_cog(ServerUtils(bot))