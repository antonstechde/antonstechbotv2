import asyncio

import discord
from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext, ButtonStyle, ComponentContext
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import wait_for_component

from utils import utils, punishments


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

    @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="punish", description="punishes a user",
                            options=pun_opt)
    async def _user_punish(self, ctx: SlashContext, user: discord.Member):
        # add moderator permission restriction
        await ctx.defer(hidden=False)
        # This command is **not** hidden, so the user can see that he is being punished
        user_setbtn1 = [
            manage_components.create_button(
                label="BAN", style=ButtonStyle.red, custom_id="ban"
            ),
            manage_components.create_button(
                label="KICK", style=ButtonStyle.red, custom_id="kick"
            ),
        ]
        user_setbtn2 = [
            manage_components.create_button(
                label="WARN", style=ButtonStyle.blue, custom_id="warn"
            ),
            manage_components.create_button(
                label="MUTE", style=ButtonStyle.blue, custom_id="mute"
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
                or not ctx.author.guild_permissions.manage_messages):
            raise discord.ext.commands.MissingPermissions  # raise some error you like
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
            buttons: ComponentContext = await wait_for_component(self.bot, components=[user_buttons_actionrow1,
                                                                                       user_buttons_actionrow2,
                                                                                       user_buttons_actionrow3],
                                                                 timeout=60,
                                                                 check=lambda msg: ctx.author.id == msg.author.id)
        except asyncio.TimeoutError:
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"] = True
                user_buttons_actionrow2["components"][i]["disabled"] = True
            user_buttons_actionrow2["components"][0]["disabled"] = True
            await message.edit(content="Timed out.", components=[user_buttons_actionrow1, user_buttons_actionrow2,
                                                                 user_buttons_actionrow3])  # Disable the Buttons
            return

        if buttons.component_id == "mute":
            mute_btn = [
                manage_components.create_button(
                    label="Minutes", style=ButtonStyle.red, custom_id="m"
                ),
                manage_components.create_button(
                    label="Hours", style=ButtonStyle.red, custom_id="h"
                ),
                manage_components.create_button(
                    label="Days", style=ButtonStyle.red, custom_id="d"
                ),
                manage_components.create_button(
                    label="Cancel", style=ButtonStyle.gray, custom_id="c"
                ),
            ]
            mute_actionrow = manage_components.create_actionrow(*mute_btn)
            await buttons.edit_origin(
                content="Do you want to mute the user for a minutes, hours or days?",
                hidden=True,
                components=[mute_actionrow],
            )
            mute_btn_ctx: ComponentContext = await manage_components.wait_for_component(
                self.bot, components=mute_actionrow, check=lambda msg: msg.author.id == buttons.author.id
            )
            if mute_btn_ctx.component_id == "c":
                for i in range(4):
                    mute_actionrow["components"][i]["disabled"] = True
                await mute_btn_ctx.edit_origin(
                    content="ok, cancelled", hidden=True, components=[mute_actionrow]
                )
            if mute_btn_ctx.component_id == "m":
                times1 = [
                    manage_components.create_button(
                        label="5", style=ButtonStyle.red, custom_id="5"
                    ),
                    manage_components.create_button(
                        label="10", style=ButtonStyle.red, custom_id="10"
                    ),
                    manage_components.create_button(
                        label="15", style=ButtonStyle.red, custom_id="15"
                    ),
                    manage_components.create_button(
                        label="20", style=ButtonStyle.red, custom_id="20"
                    ),
                ]
                times2 = [
                    manage_components.create_button(
                        label="25", style=ButtonStyle.red, custom_id="25"
                    ),
                    manage_components.create_button(
                        label="30", style=ButtonStyle.red, custom_id="30"
                    ),
                    manage_components.create_button(
                        label="35", style=ButtonStyle.red, custom_id="35"
                    ),
                    manage_components.create_button(
                        label="40", style=ButtonStyle.red, custom_id="40"
                    ),
                ]
                times3 = [
                    manage_components.create_button(
                        label="45", style=ButtonStyle.red, custom_id="45"
                    ),
                    manage_components.create_button(
                        label="50", style=ButtonStyle.red, custom_id="50"
                    ),
                    manage_components.create_button(
                        label="55", style=ButtonStyle.red, custom_id="55"
                    ),
                    manage_components.create_button(
                        label="60", style=ButtonStyle.red, custom_id="60"
                    ),
                ]

                times1_row = manage_components.create_actionrow(*times1)
                times2_row = manage_components.create_actionrow(*times2)
                times3_row = manage_components.create_actionrow(*times3)
                await mute_btn_ctx.edit_origin(
                    content="Select the duration of the mute! (timeout: 180s)",
                    hidden=True,
                    components=[times1_row, times2_row, times3_row],
                )
                try:
                    times_ctx: ComponentContext = await manage_components.wait_for_component(
                        self.bot, components=[times1_row, times2_row, times3_row],
                        check=lambda msg: msg.author.id == mute_btn_ctx.author.id, timeout=180,
                    )
                except asyncio.TimeoutError:
                    for i in range(4):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.edit_origin(
                        content="Timed out.", hidden=True, components=[times1_row, times2_row, times3_row]
                    )
                    return
                for i in range(4):
                    times1_row["components"][i]["disabled"] = True
                    times2_row["components"][i]["disabled"] = True
                    times3_row["components"][i]["disabled"] = True
                dur = int(times_ctx.component_id)
                await times_ctx.edit_origin(
                    content=f"{user.mention} is going to be muted for {dur} minutes",
                    hidden=False,
                    components=[times1_row, times2_row, times3_row],
                )
                await punishments.mute(ctx, user, dur, "m")

            if mute_btn_ctx.component_id == "h":
                times1 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="1", custom_id="1"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="2", custom_id="2"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="3", custom_id="3"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="4", custom_id="4"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="5", custom_id="5"
                    ),
                ]
                times2 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="6", custom_id="6"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="7", custom_id="7"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="8", custom_id="8"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="9", custom_id="9"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="10", custom_id="10"
                    ),
                ]
                times3 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="11", custom_id="11"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="12", custom_id="12"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="13", custom_id="13"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="14", custom_id="14"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="15", custom_id="15"
                    ),
                ]
                times4 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="16", custom_id="16"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="17", custom_id="17"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="18", custom_id="18"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="19", custom_id="19"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="20", custom_id="20"
                    ),
                ]
                times5 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="21", custom_id="21"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="22", custom_id="22"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="23", custom_id="23"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="24", custom_id="24"
                    ),
                ]

                times1_row = manage_components.create_actionrow(*times1)
                times2_row = manage_components.create_actionrow(*times2)
                times3_row = manage_components.create_actionrow(*times3)
                times4_row = manage_components.create_actionrow(*times4)
                times5_row = manage_components.create_actionrow(*times5)
                await mute_btn_ctx.edit_origin(
                    content="Select the duration of the mute! (timeout: 180s)",
                    hidden=True,
                    components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                )
                try:
                    times_ctx: ComponentContext = await manage_components.wait_for_component(
                        self.bot,
                        components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                        check=lambda msg: mute_btn_ctx.author.id == msg.author.id,
                        timeout=180
                    )
                except asyncio.TimeoutError:
                    for i in range(5):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                        times4_row["components"][i]["disabled"] = True
                    for i in range(4):
                        times5_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.edit_origin(
                        content="Timed out.", hidden=True, 
                        components=[times1_row, times2_row, times3_row, times4_row, times5_row]
                    )
                    return
                for i in range(5):
                    times1_row["components"][i]["disabled"] = True
                    times2_row["components"][i]["disabled"] = True
                    times3_row["components"][i]["disabled"] = True
                    times4_row["components"][i]["disabled"] = True
                for i in range(4):
                    times5_row["components"][i]["disabled"] = True
                dur = int(times_ctx.component_id)
                await times_ctx.edit_origin(
                    content=f"{user.mention} is going to be muted for {dur} hours",
                    hidden=False,
                    components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                )
                await punishments.mute(ctx, user, dur, "h")
            if mute_btn_ctx.component_id == "d":
                times1 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="1", custom_id="1"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="2", custom_id="2"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="3", custom_id="3"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="4", custom_id="4"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="5", custom_id="5"
                    ),
                ]
                times2 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="6", custom_id="6"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="7", custom_id="7"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="8", custom_id="8"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="9", custom_id="9"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="10", custom_id="10"
                    ),
                ]
                times3 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="11", custom_id="11"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="12", custom_id="12"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="13", custom_id="13"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="14", custom_id="14"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="15", custom_id="15"
                    ),
                ]
                times4 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="16", custom_id="16"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="17", custom_id="17"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="18", custom_id="18"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="19", custom_id="19"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="20", custom_id="20"
                    ),
                ]
                times5 = [
                    manage_components.create_button(
                        style=ButtonStyle.red, label="21", custom_id="21"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="22", custom_id="22"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="23", custom_id="23"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="24", custom_id="24"
                    ),
                    manage_components.create_button(
                        style=ButtonStyle.red, label="25", custom_id="25"
                    ),
                ]
                times1_row = manage_components.create_actionrow(*times1)
                times2_row = manage_components.create_actionrow(*times2)
                times3_row = manage_components.create_actionrow(*times3)
                times4_row = manage_components.create_actionrow(*times4)
                times5_row = manage_components.create_actionrow(*times5)
                await mute_btn_ctx.edit_origin(
                    content="Select the duration of the mute! (timeout: 180s)",
                    hidden=True,
                    components=[times1_row, times2_row, times3_row, times4_row, times5_row]
                )
                try:
                    times_ctx: ComponentContext = await manage_components.wait_for_component(
                        self.bot,
                        components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                        check=lambda msg: mute_btn_ctx.author.id == msg.author.id,
                        timeout=180
                    )
                except asyncio.TimeoutError:
                    for i in range(5):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                        times4_row["components"][i]["disabled"] = True
                        times5_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.edit_origin(
                        content="Timed out.", hidden=True, 
                        components=[times1_row, times2_row, times3_row, times4_row, times5_row]
                    )
                    return
                for i in range(5):
                    times1_row["components"][i]["disabled"] = True
                    times2_row["components"][i]["disabled"] = True
                    times3_row["components"][i]["disabled"] = True
                    times4_row["components"][i]["disabled"] = True
                    times5_row["components"][i]["disabled"] = True
                dur = int(times_ctx.component_id)
                await times_ctx.edit_origin(
                    content=f"{user.mention} is going to be muted for {dur} days",
                    hidden=False,
                    components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                )
                await punishments.mute(ctx, user, dur, "d")

        if buttons.component_id == "warn":
            await buttons.edit_origin(content="please send a message with the reason of the warning! (timeout: 600s)",
                                      components=[])
            try:
                a = self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id, timeout=600)
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.warn(ctx, user, reason)

        if buttons.component_id == "kick":
            await buttons.edit_origin(content="please send a message with the reason of the kick! (timeout: 600s)",
                                      components=[])
            try:
                a = self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id, timeout=600)
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.kick(ctx, user, reason)

        if buttons.component_id == "ban":
            await buttons.edit_origin(content="please send a message with the reason of the ban! (timeout: 600s)",
                                      components=[])
            try:
                a = self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id, timeout=600)
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.ban(ctx, user, reason)

    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="un-punish", description="un-punishes a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="unban", description="unbans a user")
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
