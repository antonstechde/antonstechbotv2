import asyncio
import re
import traceback
from typing import Union

import discord
from discord.ext.commands import AutoShardedBot, Cog
from discord_slash import ButtonStyle, ComponentContext, SlashContext, cog_ext
from discord_slash.utils import manage_components

from utils import punishments, utils


class ServerUtils(Cog):
    """
    This class is supposed to contain a lot of server based stuff like "channel create/delete" or "user punish/unpunish"
    """

    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    async def _get_role_permissions(self, ctx: ComponentContext, roleperm):
        sel = manage_components.create_select(
            placeholder="Choose the permissions you want for your role (1/2)",
            min_values=1,
            max_values=18,
            options=[
                manage_components.create_select_option(
                    label="add reactions to messages",
                    value="add_reactions",
                ),
                manage_components.create_select_option(
                    label="attach files to messages",
                    value="attach_files",
                ),
                manage_components.create_select_option(
                    label="ban members",
                    value="ban_members",
                ),
                manage_components.create_select_option(
                    label="change own nickname",
                    value="change_nickname",
                ),
                manage_components.create_select_option(
                    label="connect to voice channels",
                    value="connect",
                ),
                manage_components.create_select_option(
                    label="create instant invite to a channel",
                    value="create_instant_invite",
                ),
                manage_components.create_select_option(
                    label="deafen other members in voice channels",
                    value="deafen_members",
                ),
                manage_components.create_select_option(
                    label="embed links in channels",
                    value="embed_links",
                ),
                manage_components.create_select_option(
                    label="send external emojis",
                    value="external_emojis",
                ),
                manage_components.create_select_option(
                    label="kick members",
                    value="kick_members",
                ),
                manage_components.create_select_option(
                    label="manage channels on the server",
                    value="manage_channels",
                ),
                manage_components.create_select_option(
                    label="manage emojis of the server",
                    value="manage_emojis",
                ),
                manage_components.create_select_option(
                    label="manage guild",
                    value="manage_guild",
                ),
                manage_components.create_select_option(
                    label="manage messages",
                    value="manage_messages",
                ),
                manage_components.create_select_option(
                    label="manage all nicknames",
                    value="manage_nicknames",
                ),
                manage_components.create_select_option(
                    label="manage the permission of roles",
                    value="manage_permissions",
                ),
                manage_components.create_select_option(
                    label="manage roles and their permissions",
                    value="manage_roles",
                ),
                manage_components.create_select_option(
                    label="manage webhooks", value="manage_webhooks"
                ),
            ],
        )
        selrow = manage_components.create_actionrow(sel)
        await ctx.edit_origin(
            content="Please choose the permissions you want to assign to the role (1/2)",
            components=[selrow],
        )

        try:
            firstperms = await manage_components.wait_for_component(
                self.bot,
                components=[selrow],
                timeout=600,
                check=lambda msg: msg.author.id == ctx.author.id,
            )
            await firstperms.defer(edit_origin=True)
        except asyncio.TimeoutError:
            selrow["components"][0]["disabled"] = True
            await ctx.origin_message.edit("Timed out.", components=[selrow])
            return

        roleperm.add_reactions = True if "add_reactions" in firstperms.selected_options else False
        roleperm.attach_files = True if "attach_files" in firstperms.selected_options else False
        roleperm.ban_members = True if "ban_members" in firstperms.selected_options else False
        roleperm.change_nickname = (
            True if "change_nickname" in firstperms.selected_options else False
        )
        roleperm.connect = True if "connect" in firstperms.selected_options else False
        roleperm.create_instant_invite = (
            True if "create_instant_invite" in firstperms.selected_options else False
        )
        roleperm.deafen_members = True if "deafen_members" in firstperms.selected_options else False
        roleperm.embed_links = True if "embed_links" in firstperms.selected_options else False
        roleperm.external_emojis = (
            True if "external_emojis" in firstperms.selected_options else False
        )
        roleperm.kick_members = True if "kick_members" in firstperms.selected_options else False
        roleperm.manage_channels = (
            True if "manage_channels" in firstperms.selected_options else False
        )
        roleperm.manage_emojis = True if "manage_emojis" in firstperms.selected_options else False
        roleperm.manage_guild = True if "manage_guild" in firstperms.selected_options else False
        roleperm.manage_messages = (
            True if "manage_messages" in firstperms.selected_options else False
        )
        roleperm.manage_nicknames = (
            True if "manage_nicknames" in firstperms.selected_options else False
        )
        roleperm.manage_permissions = (
            True if "manage_permissions" in firstperms.selected_options else False
        )
        roleperm.manage_roles = True if "manage_roles" in firstperms.selected_options else False
        roleperm.manage_webhooks = (
            True if "manage_webhooks" in firstperms.selected_options else False
        )

        sel2 = manage_components.create_select(
            placeholder="Choose the permissions you want for your role (2/2)",
            max_values=17,
            min_values=1,
            options=[
                manage_components.create_select_option(
                    label="mention everyone in a message",
                    value="mention_everyone",
                ),
                manage_components.create_select_option(
                    label="move members across voice channels",
                    value="move_members",
                ),
                manage_components.create_select_option(
                    label="mute members in voice channels",
                    value="mute_members",
                ),
                manage_components.create_select_option(
                    label="priority speaker",
                    value="priority_speaker",
                ),
                manage_components.create_select_option(
                    label="read message history in channels",
                    value="read_message_history",
                ),
                manage_components.create_select_option(
                    label="read all messages in channels",
                    value="read_messages",
                ),
                manage_components.create_select_option(
                    label="request to speak in stage channels",
                    value="request_to_speak",
                ),
                manage_components.create_select_option(
                    label="send messages in channels",
                    value="send_messages",
                ),
                manage_components.create_select_option(
                    label="send TTS messages in channels",
                    value="send_tts_messages",
                ),
                manage_components.create_select_option(
                    label="speak in voice channels",
                    value="speak",
                ),
                manage_components.create_select_option(
                    label="stream in voice channels / enable camera",
                    value="stream",
                ),
                manage_components.create_select_option(
                    label="use external emojis",
                    value="use_external_emojis",
                ),
                manage_components.create_select_option(
                    label="use slash commands in channels",
                    value="use_slash_commands",
                ),
                manage_components.create_select_option(
                    label="use voice activation in voice channels (else only push-to-talk)",
                    value="use_voice_activation",
                ),
                manage_components.create_select_option(
                    label="view the audit-log",
                    value="view_audit_log",
                ),
                manage_components.create_select_option(
                    label="view channels",
                    value="view_channel",
                ),
                manage_components.create_select_option(
                    label="view guild insights",
                    value="view_guild_insights",
                ),
            ],
        )
        sel2row = manage_components.create_actionrow(sel2)
        await firstperms.edit_origin(
            content="Please choose the permissions you want to assign to the role (2/2)",
            components=[sel2row],
        )

        try:
            secondperms = await manage_components.wait_for_component(
                self.bot,
                components=[sel2row],
                timeout=600,
                check=lambda msg: msg.author.id == ctx.author.id,
            )
            await secondperms.defer(edit_origin=True)
        except asyncio.TimeoutError:
            sel2row["components"][0]["disabled"] = True
            await firstperms.origin_message.edit("Timed out.", components=[sel2row])
            return

        roleperm.mention_everyone = (
            True if "mention_everyone" in secondperms.selected_options else False
        )
        roleperm.move_members = True if "move_members" in secondperms.selected_options else False
        roleperm.mute_members = True if "mute_members" in secondperms.selected_options else False
        roleperm.priority_speaker = (
            True if "priority_speaker" in secondperms.selected_options else False
        )
        roleperm.read_message_history = (
            True if "read_message_history" in secondperms.selected_options else False
        )
        roleperm.read_messages = True if "read_messages" in secondperms.selected_options else False
        roleperm.request_to_speak = (
            True if "request_to_speak" in secondperms.selected_options else False
        )
        roleperm.send_messages = True if "send_messages" in secondperms.selected_options else False
        roleperm.send_tts_messages = (
            True if "send_tts_messages" in secondperms.selected_options else False
        )
        roleperm.speak = True if "speak" in secondperms.selected_options else False
        roleperm.stream = True if "stream" in secondperms.selected_options else False
        roleperm.use_external_emojis = (
            True if "use_external_emojis" in secondperms.selected_options else False
        )
        roleperm.use_slash_commands = (
            True if "use_slash_commands" in secondperms.selected_options else False
        )
        roleperm.use_voice_activation = (
            True if "use_voice_activation" in secondperms.selected_options else False
        )
        roleperm.view_audit_log = (
            True if "view_audit_log" in secondperms.selected_options else False
        )
        roleperm.view_channel = True if "view_channel" in secondperms.selected_options else False
        roleperm.view_guild_insights = (
            True if "view_guild_insights" in secondperms.selected_options else False
        )

        return roleperm, sel2row, secondperms

    pun_opt = [{"name": "user", "description": "The user to punish", "required": True, "type": 6}]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="user",
        name="punish",
        description="punishes a user",
        options=pun_opt,
    )
    async def _user_punish(self, ctx: SlashContext, user: discord.Member):
        # add moderator permission restriction
        await ctx.defer(hidden=False)
        # This command is **not** hidden, so the user can see that he is being punished
        user_setbtn1 = [
            manage_components.create_button(label="BAN", style=ButtonStyle.red, custom_id="ban"),
            manage_components.create_button(label="KICK", style=ButtonStyle.red, custom_id="kick"),
        ]
        user_setbtn2 = [
            manage_components.create_button(label="WARN", style=ButtonStyle.blue, custom_id="warn"),
            manage_components.create_button(label="MUTE", style=ButtonStyle.blue, custom_id="mute"),
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
            and not ctx.author.guild_permissions.kick_members
            and not ctx.author.guild_permissions.manage_messages
        ):
            raise discord.ext.commands.MissingPermissions(
                missing_perms=["manage_messages", "ban_members", "kick_members"]
            )  # raise some error you like

        if (
            not ctx.author.guild_permissions.ban_members
            or not ctx.author.guild_permissions.kick_members
        ):
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"] = True
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
            buttons: ComponentContext = await manage_components.wait_for_component(
                self.bot,
                components=[
                    user_buttons_actionrow1,
                    user_buttons_actionrow2,
                    user_buttons_actionrow3,
                ],
                timeout=60,
                check=lambda msg: ctx.author.id == msg.author.id,
            )
            await buttons.defer(edit_origin=True)
        except asyncio.TimeoutError:
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"] = True
                user_buttons_actionrow2["components"][i]["disabled"] = True
            user_buttons_actionrow3["components"][0]["disabled"] = True
            await message.edit(
                content="Timed out.",
                components=[
                    user_buttons_actionrow1,
                    user_buttons_actionrow2,
                    user_buttons_actionrow3,
                ],
            )  # Disable the Buttons
            return

        if buttons.component_id == "mute":
            mute_btn = [
                manage_components.create_button(
                    label="Minutes", style=ButtonStyle.red, custom_id="m"
                ),
                manage_components.create_button(
                    label="Hours", style=ButtonStyle.red, custom_id="h"
                ),
                manage_components.create_button(label="Days", style=ButtonStyle.red, custom_id="d"),
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
            mute_btn_ctx: ComponentContext = (
                await manage_components.manage_components.wait_for_component(
                    self.bot,
                    components=mute_actionrow,
                    check=lambda msg: msg.author.id == buttons.author.id,
                )
            )
            await mute_btn_ctx.defer(edit_origin=True)
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
                    times_ctx: ComponentContext = (
                        await manage_components.manage_components.wait_for_component(
                            self.bot,
                            components=[times1_row, times2_row, times3_row],
                            check=lambda msg: msg.author.id == mute_btn_ctx.author.id,
                            timeout=180,
                        )
                    )
                    await times_ctx.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    for i in range(4):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.origin_message.edit(
                        content="Timed out.",
                        hidden=True,
                        components=[times1_row, times2_row, times3_row],
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
                    times_ctx: ComponentContext = (
                        await manage_components.manage_components.wait_for_component(
                            self.bot,
                            components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                            check=lambda msg: mute_btn_ctx.author.id == msg.author.id,
                            timeout=180,
                        )
                    )
                    await times_ctx.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    for i in range(5):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                        times4_row["components"][i]["disabled"] = True
                    for i in range(4):
                        times5_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.origin_message.edit(
                        content="Timed out.",
                        hidden=True,
                        components=[times1_row, times2_row, times3_row, times4_row, times5_row],
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
                    components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                )
                try:
                    times_ctx: ComponentContext = (
                        await manage_components.manage_components.wait_for_component(
                            self.bot,
                            components=[times1_row, times2_row, times3_row, times4_row, times5_row],
                            check=lambda msg: mute_btn_ctx.author.id == msg.author.id,
                            timeout=180,
                        )
                    )
                    await times_ctx.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    for i in range(5):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                        times4_row["components"][i]["disabled"] = True
                        times5_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.origin_message.edit(
                        content="Timed out.",
                        hidden=True,
                        components=[times1_row, times2_row, times3_row, times4_row, times5_row],
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
            await buttons.edit_origin(
                content="please send a message with the reason of the warning! (timeout: 600s)",
                components=[],
            )
            try:
                a = await self.bot.wait_for(
                    "message", check=lambda msg: msg.author.id == buttons.author.id, timeout=600
                )
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.warn(ctx, user, reason)

        if buttons.component_id == "kick":
            await buttons.edit_origin(
                content="please send a message with the reason of the kick! (timeout: 600s)",
                components=[],
            )
            try:
                a = await self.bot.wait_for(
                    "message", check=lambda msg: msg.author.id == buttons.author.id, timeout=600
                )
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.kick(ctx, user, reason)

        if buttons.component_id == "ban":
            await buttons.edit_origin(
                content="please send a message with the reason of the ban! (timeout: 600s)",
                components=[],
            )
            try:
                a = await self.bot.wait_for(
                    "message", check=lambda msg: msg.author.id == buttons.author.id, timeout=600
                )
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.ban(ctx, user, reason)

        if buttons.component_id == "nothing":
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"] = True
                user_buttons_actionrow2["components"][i]["disabled"] = True
            user_buttons_actionrow3["components"][0]["disabled"] = True
            await buttons.edit_origin(
                content="ok nothing will happen",
                components=[
                    user_buttons_actionrow1,
                    user_buttons_actionrow2,
                    user_buttons_actionrow3,
                ],
            )

    @cog_ext.cog_subcommand(
        base="server", subcommand_group="user", name="unban", description="unbans a user"
    )
    async def _unban(
        self, ctx: SlashContext, user_id: str, reason: str
    ):  # in theory discord-slash should automatically create options for that
        user_id = int(user_id)
        user: discord.User = await self.bot.fetch_user(user_id)
        reason1 = f"User {ctx.author.name} used the unban command on {user.name}! \n Unban-Reason: {reason}"
        await ctx.guild.unban(user=user, reason=reason1)
        await ctx.send(f"unbanned {user.mention}!")

    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="un-punish", description="un-punishes a user")   # TODO: work on this when mute and warn system done

    radd_opt = [
        {
            "name": "user",
            "description": "the user to add the role to",
            "required": True,
            "type": 6,
        },
        {
            "name": "role",
            "description": "the role to add",
            "type": 8,
            "required": True,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="user",
        name="add-role",
        description="adds a role to a user",
        options=radd_opt,
    )
    async def _role_add(self, ctx: SlashContext, user: discord.Member, role: discord.Role):
        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_roles"])
        await user.add_roles(
            role, reason=f"User {ctx.author.name} used the add-role command on {user.name}!"
        )
        await ctx.send("Done!")

    rrem_opt = [
        {
            "name": "user",
            "description": "the user to remove the role from",
            "required": True,
            "type": 6,
        },
        {
            "name": "role",
            "description": "the role to remove",
            "type": 8,
            "required": True,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="user",
        name="remove-role",
        description="removes a role from a user",
        options=rrem_opt,
    )
    async def _role_remove(self, ctx: SlashContext, user: discord.Member, role: discord.Role):
        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_roles"])
        await user.remove_roles(
            role, reason=f"User {ctx.author.name} used the remove-role command on {user.name}!"
        )
        await ctx.send("Done!")

    rcre_opt = [
        {
            "name": "name",
            "description": "the name of the role",
            "required": True,
            "type": 3,
        },
        {
            "name": "color",
            "description": "the colour of the role (hex code)",
            "type": 3,
            "required": True,
        },
        {
            "name": "hoist",
            "description": "whether the role should be shown separately in the member list, default False",
            "required": False,
            "type": 5,
        },
        {
            "name": "mentionable",
            "description": "whether everyone should be able to mention the role, default False",
            "required": False,
            "type": 5,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="role",
        name="create",
        description="creates a role",
        options=rcre_opt,
    )
    async def _create_role(
        self,
        ctx: SlashContext,
        name: str,
        color: str,
        hoist: bool = False,
        mentionable: bool = False,
    ):
        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.errors.MissingPermissions(missing_perms=["manage_roles"])
        match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)  # check if color is hex
        if not match:
            raise discord.ext.commands.BadArgument("color is not a hex-color code")
        hexval = color.lstrip("#")
        rgbval = tuple(bytes.fromhex(hexval))
        await ctx.defer(hidden=False)

        roleperm = discord.Permissions().none()
        color = discord.Colour.from_rgb(r=rgbval[0], g=rgbval[1], b=rgbval[2])

        anypermbutton = [
            manage_components.create_button(label="Yes", style=ButtonStyle.green, custom_id="yes"),
            manage_components.create_button(label="No", style=ButtonStyle.red, custom_id="no"),
        ]

        adminbutton = [
            manage_components.create_button(label="Yes", style=ButtonStyle.green, custom_id="yes"),
            manage_components.create_button(label="No", style=ButtonStyle.red, custom_id="no"),
        ]
        any_ar = manage_components.create_actionrow(*anypermbutton)
        adm_ar = manage_components.create_actionrow(*adminbutton)

        ask = await ctx.send(
            "Do you want to have any Permission enabled on your role?", components=[any_ar]
        )

        try:
            answer: ComponentContext = await manage_components.wait_for_component(
                self.bot,
                components=[any_ar],
                timeout=600,
                check=lambda msg: ctx.author.id == msg.author.id,
            )
            await answer.defer(edit_origin=True)
        except asyncio.TimeoutError:
            for i in range(2):
                any_ar["components"][i]["disabled"] = True
            await ask.edit(content="Timed out.", components=[any_ar])
            return

        if answer.component_id == "no":
            for i in range(2):
                any_ar["components"][i]["disabled"] = True
            await answer.edit_origin(
                content=f"creating role '{name}' with the color #{hexval} and no permissions....",
                components=[any_ar],
            )
            await ctx.guild.create_role(
                name=name,
                color=color,
                permissions=roleperm,
                hoist=hoist,
                mentionable=mentionable,
                reason=f"User {ctx.author.name} used the create-role command!",
            )
            await ctx.channel.send("Done")
            return

        else:
            pass

        await answer.edit_origin(
            content="Do you want the role to have administrator-permissions?", components=[adm_ar]
        )
        try:
            admin: ComponentContext = await manage_components.wait_for_component(
                self.bot,
                components=[adm_ar],
                timeout=600,
                check=lambda msg: msg.author.id == ctx.author.id,
            )
            await admin.defer(edit_origin=True)
        except asyncio.TimeoutError:
            for i in range(2):
                adm_ar["components"][i]["disabled"] = True
            await answer.origin_message.edit(content="Timed out.", components=[adm_ar])
            return

        if admin.component_id == "yes":
            roleperm.administrator = True
            for i in range(2):
                adm_ar["components"][i]["disabled"] = True
            await admin.edit_origin(
                content=f"creating role '{name}' with the color #{hexval} and administrator permissions....",
                components=[adm_ar],
            )
            await ctx.guild.create_role(
                name=name,
                color=color,
                permissions=roleperm,
                hoist=hoist,
                mentionable=mentionable,
                reason=f"User {ctx.author.name} used the create-role command!",
            )
            await ctx.channel.send("Done")
            return

        else:
            try:
                roleperm, sel2row, secondperms = await self._get_role_permissions(
                    ctx=admin, roleperm=roleperm
                )
            except ValueError:  # on timeout no values returned, just do nothing then
                return

        sel2row["components"][0]["disabled"] = True
        await secondperms.edit_origin(
            content=f"Role '{name}' with color #{hexval} and your custom permissions, which have the value {roleperm.value}, is being created",
            components=[sel2row],
        ),
        await ctx.guild.create_role(
            name=name,
            color=color,
            permissions=roleperm,
            hoist=hoist,
            mentionable=mentionable,
            reason=f"User {ctx.author.name} used the create-role command!",
        )

        await ctx.channel.send("Done!")

    redt_opt = [
        {
            "name": "role",
            "description": "the role you want to edit",
            "required": True,
            "type": 8,
        },
        {
            "name": "name",
            "description": "the new name of the role",
            "required": False,
            "type": 3,
        },
        {
            "name": "color",
            "description": "the new colour of the role (hex code)",
            "type": 3,
            "required": False,
        },
        {
            "name": "hoist",
            "description": "whether the role should be shown separately in the member list",
            "required": False,
            "type": 5,
        },
        {
            "name": "mentionable",
            "description": "whether everyone should be able to mention the role",
            "required": False,
            "type": 5,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="role",
        name="edit",
        description="edits a role",
        options=redt_opt,
    )
    async def _role_edit(
        self,
        ctx: SlashContext,
        role: discord.Role,
        name: str = None,
        color: str = None,
        hoist: bool = None,
        mentionable: bool = None,
    ):

        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.errors.MissingPermissions(missing_perms=["manage_roles"])

        if not name:
            name = role.name

        if not hoist:
            hoist = role.hoist

        if not mentionable:
            mentionable = role.mentionable

        if color:
            match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)  # check if color is hex
            if not match:
                raise discord.ext.commands.BadArgument("color is not a hex-color code")
            await ctx.defer(hidden=False)
            hexval = color.lstrip("#")
            rgbval = tuple(bytes.fromhex(hexval))
            color = discord.Colour.from_rgb(r=rgbval[0], g=rgbval[1], b=rgbval[2])

        elif not color:
            await ctx.defer(hidden=False)
            color = role.colour

        perm_edt = [
            manage_components.create_button(
                label="Yes",
                style=ButtonStyle.green,
                custom_id="yes",
            ),
            manage_components.create_button(
                label="No",
                style=ButtonStyle.red,
                custom_id="no",
            ),
        ]

        perm_ar = manage_components.create_actionrow(*perm_edt)
        adminbutton = [
            manage_components.create_button(label="Yes", style=ButtonStyle.green, custom_id="yes"),
            manage_components.create_button(label="No", style=ButtonStyle.red, custom_id="no"),
        ]
        adm_ar = manage_components.create_actionrow(*adminbutton)

        msg = await ctx.send(
            "Do you want to edit the permissions of the role?", components=[perm_ar]
        )

        try:
            perm: ComponentContext = await manage_components.wait_for_component(
                self.bot,
                components=[perm_ar],
                timeout=600,
                check=lambda m: m.author.id == ctx.author.id,
            )
            await perm.defer(edit_origin=True)

        except asyncio.TimeoutError:
            for i in range(2):
                perm_ar["components"][i]["disabled"] = True
            await msg.edit(content="Timed out.", components=[perm_ar])
            return

        if perm.custom_id == "no":
            roleperm = role.permissions
            for i in range(2):
                perm_ar["components"][i]["disabled"] = True
            await perm.edit_origin(
                content="editing the role without changing permissions?", components=[perm_ar]
            )
            await role.edit(
                permissions=roleperm,
                name=name,
                hoist=hoist,
                mentionable=mentionable,
                colour=color,
                reason=f"User {ctx.author.name} used the role-edit command!",
            )
            await perm.origin_message.channel.send(content="Done")
            return

        else:
            await perm.edit_origin(
                content="Do you want the role to have administrator-permissions?",
                components=[adm_ar],
            )
            try:
                admin: ComponentContext = await manage_components.wait_for_component(
                    self.bot,
                    components=[adm_ar],
                    timeout=600,
                    check=lambda msg: msg.author.id == ctx.author.id,
                )
                await admin.defer(edit_origin=True)
            except asyncio.TimeoutError:
                for i in range(2):
                    adm_ar["components"][i]["disabled"] = True
                await perm.origin_message.edit(content="Timed out.", components=[adm_ar])
                return

            if admin.component_id == "yes":
                roleperm = discord.Permissions().none()
                roleperm.administrator = True
                for i in range(2):
                    adm_ar["components"][i]["disabled"] = True
                await admin.edit_origin(
                    content="editing role to admin-permissions", components=[adm_ar]
                )
                await role.edit(
                    name=name,
                    color=color,
                    permissions=roleperm,
                    hoist=hoist,
                    mentionable=mentionable,
                    reason=f"User {ctx.author.name} used the role-edit command!",
                )
                await admin.origin_message.channel.send("Done")
                return

            else:
                try:
                    roleperm = discord.Permissions().none()
                    roleperm, sel2row, secondperms = await self._get_role_permissions(
                        ctx=admin, roleperm=roleperm
                    )

                    sel2row["components"][0]["disabled"] = True

                    await secondperms.edit_origin(
                        components=[sel2row], content="Edting role to your input....."
                    )

                    await role.edit(
                        name=name,
                        hoist=hoist,
                        colour=color,
                        mentionable=mentionable,
                        permissions=roleperm,
                        reason=f"User {ctx.author.name} used the role-edit command!",
                    )
                    await secondperms.origin_message.channel.send(content="Done")
                except ValueError:  # on timeout no values returned, just do nothing then
                    return

    rdel_opt = [
        {
            "name": "role",
            "description": "the role to delete",
            "required": True,
            "type": 8,
        }
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="role",
        name="delete",
        description="deletes a role",
        options=rdel_opt,
    )
    async def _delete_role(self, ctx: SlashContext, role: discord.Role):
        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_roles"])
        await role.delete(reason=f"User {ctx.author.name} used the role-delete command!")
        await ctx.send("role has been deleted", hidden=True)

    ch_cre_opt = [
        {
            "name": "channel_type",
            "description": "Text or Voice Channel",
            "required": True,
            "type": 3,
            "choices": [
                {
                    "name": "Text-channel",
                    "value": "TextChannel",
                },
                {
                    "name": "Voice-channel",
                    "value": "VoiceChannel",
                },
            ],
        },
        {
            "name": "name",
            "description": "the name of the channel",
            "type": 3,
            "required": True,
        },
        {
            "name": "category",
            "description": "the category to add the channel to",
            "type": 7,
            "required": True,
        },
        {
            "name": "nsfw",
            "description": "whether the channel is nsfw. Default False (Text-Channel only)",
            "type": 5,
            "required": False,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="channel",
        name="create",
        description="creates a channel",
        options=ch_cre_opt,
    )
    async def _channel_create(
        self,
        ctx: SlashContext,
        channel_type: str,
        name: str,
        category: discord.CategoryChannel,
        nsfw: bool = False,
    ):
        if not ctx.author.guild_permissions.manage_channels:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_channels"])
        await ctx.defer(hidden=True)
        if channel_type == "TextChannel":
            await ctx.guild.create_text_channel(
                name=name,
                category=category,
                nsfw=nsfw,
                reason=f"User {ctx.author.name} used the channel-create command!",
            )

        elif channel_type == "VoiceChannel":
            await ctx.guild.create_voice_channel(
                name=name,
                category=category,
                reason=f"User {ctx.author.name} used the channel-create command!",
            )
        await ctx.send("done", hidden=True)

    ch_edt_opt = [
        {
            "name": "channel",
            "description": "The channel to edit",
            "type": 7,
            "required": True,
        },
        {
            "name": "name",
            "description": "The new name of the channel",
            "type": 3,
            "required": False,
        },
        {
            "name": "slowmode_delay",
            "description": "set the slowmode for the channel (only for text channels)",
            "type": 4,
            "required": False,
        },
        {
            "name": "max_user_count",
            "description": "set the max user count for the channel (only for voice channels",
            "type": 4,
            "required": False,
        },
        {
            "name": "nsfw",
            "description": "whether the channel is nsfw. (Text-Channel only)",
            "type": 5,
            "required": False,
        },
        {
            "name": "position",
            "description": "the position of the channel",
            "type": 4,
            "required": False,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="channel",
        name="edit",
        description="edits a channel",
        options=ch_edt_opt,
    )
    async def _channel_edit(
        self,
        ctx: SlashContext,
        channel: Union[discord.TextChannel, discord.VoiceChannel],
        name: str = None,
        slowmode_delay: int = None,
        max_user_count: int = None,
        nsfw: bool = None,
        position: int = None,
    ):
        if not ctx.author.guild_permissions.manage_channels:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_channels"])
        await ctx.defer(hidden=True)
        if isinstance(channel, discord.TextChannel):
            await channel.edit(
                name=name if name is not None else channel.name,
                slowmode_delay=slowmode_delay
                if slowmode_delay is not None
                else channel.slowmode_delay,
                nsfw=nsfw if nsfw is not None else channel.nsfw,
                position=position if nsfw is not None else channel.position,
                reason=f"User {ctx.author.name} used the channel-edit command!",
            )
        elif isinstance(channel, discord.VoiceChannel):
            await channel.edit(
                name=name if name is not None else channel.name,
                user_limit=max_user_count if max_user_count is not None else channel.user_limit,
                position=position if nsfw is not None else channel.position,
                reason=f"User {ctx.author.name} used the channel-edit command!",
            )
        await ctx.send("done", hidden=True)

    ch_perm_edt_opt = [
        {
            "name": "channel",
            "description": "the channel update permissions on",
            "type": 7,
            "required": True,
        },
        {
            "name": "role_or_user",
            "description": "the role or user to give special permissions over a channel",
            "type": 9,
            "required": True,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="channel",
        name="permission_edit",
        options=ch_perm_edt_opt,
        description="edits the permissions a user or a role has in a specific channel",
    )
    async def _channel_permission_edit(
        self,
        ctx: SlashContext,
        channel: Union[discord.TextChannel, discord.VoiceChannel],
        role_or_user: Union[discord.Role, discord.Member],
    ):
        if (
            not ctx.author.guild_permissions.manage_channels
            and not ctx.author.guild_permissions.manage_permissions
        ):
            raise discord.ext.commands.MissingPermissions(
                missing_perms=["manage_channels", "manage_permissions"]
            )

        else:
            await ctx.defer(hidden=False)

        if isinstance(channel, discord.TextChannel):
            utils.LOGGER.debug(f"Test: {isinstance(role_or_user, str)} \n value: {role_or_user}")
            perm_sel = manage_components.create_select(
                min_values=1,
                max_values=14,
                placeholder=f"choose the permissions to give the {'user' if isinstance(role_or_user, discord.Member) else 'role'}",
                options=[
                    manage_components.create_select_option(
                        label="view the channel",
                        value="view_channel",
                    ),
                    manage_components.create_select_option(
                        label="manage the channel",
                        value="manage_channels",
                    ),
                    manage_components.create_select_option(
                        label="manage channel permissions",
                        value="manage_permissions",
                    ),
                    manage_components.create_select_option(
                        label="manage webhooks",
                        value="manage_webhooks",
                    ),
                    manage_components.create_select_option(
                        label="create instant invite",
                        value="create_instant_invite",
                    ),
                    manage_components.create_select_option(
                        label="send messages in the channel",
                        value="send_messages",
                    ),
                    manage_components.create_select_option(
                        label="embed links in messages",
                        value="embed_links",
                    ),
                    manage_components.create_select_option(
                        label="attach files to messages",
                        value="attach_files",
                    ),
                    manage_components.create_select_option(
                        label="add reactions to messages",
                        value="add_reactions",
                    ),
                    manage_components.create_select_option(
                        label="use external emojis in messages",
                        value="use_external_emojis",
                    ),
                    manage_components.create_select_option(
                        label="mention @everyone",
                        value="mention_everyone",
                    ),
                    manage_components.create_select_option(
                        label="manage messages",
                        value="manage_messages",
                    ),
                    manage_components.create_select_option(
                        label="read message history",
                        value="read_message_history",
                    ),
                    manage_components.create_select_option(
                        label="send tts messages",
                        value="send_tts_messages",
                    ),
                ],
            )
            sel_ar = manage_components.create_actionrow(perm_sel)
            msg = await ctx.send(
                content=f"What Permissions do you want to give the {'user' if isinstance(role_or_user, discord.Member) else 'role'}\n"
                f"all not selected permissions will be **denied**",
                components=[sel_ar],
            )

            try:
                perms: ComponentContext = await manage_components.wait_for_component(
                    self.bot,
                    components=[sel_ar],
                    timeout=600,
                    check=lambda p: p.author.id == ctx.author.id,
                )
                await perms.defer(edit_origin=True)
            except asyncio.TimeoutError:
                sel_ar["components"][0]["disabled"] = True
                await msg.edit(content="Timed out.", components=[sel_ar])
                return

            perm = discord.PermissionOverwrite(
                view_channel=True if "view_channel" in perms.selected_options else False,
                manage_channels=True if "manage_channels" in perms.selected_options else False,
                manage_permissions=True
                if "manage_permissions" in perms.selected_options
                else False,
                manage_webhooks=True if "manage_webhooks" in perms.selected_options else False,
                create_instant_invite=True
                if "create_instant_invite" in perms.selected_options
                else False,
                send_messages=True if "send_messages" in perms.selected_options else False,
                embed_links=True if "embed_links" in perms.selected_options else False,
                attach_files=True if "attach_files" in perms.selected_options else False,
                add_reactions=True if "add_reactions" in perms.selected_options else False,
                use_external_emojis=True
                if "use_external_emojis" in perms.selected_options
                else False,
                mention_everyone=True if "mention_everyone" in perms.selected_options else False,
                manage_messages=True if "manage_messages" in perms.selected_options else False,
                read_message_history=True
                if "read_message_history" in perms.selected_options
                else False,
                send_tts_messages=True if "send_tts_messages" in perms.selected_options else False,
            )

            sel_ar["components"][0]["disabled"] = True

            try:

                await perms.edit_origin(
                    content="Editing channel permissions....", components=[sel_ar]
                )

                utils.LOGGER.debug(f"type: {type(role_or_user)}")

                perm_overwrite = {role_or_user: perm}
                await channel.edit(
                    overwrites=perm_overwrite,
                    reason=f"User {ctx.author.name} used the channel-permission-edit command!",
                )
                await perms.channel.send(
                    f"Done, channel '{channel.name} has been edited!", delete_after=180
                )
            except AttributeError:
                error = traceback.format_exc()
                utils.LOGGER.error(error)

        elif isinstance(channel, discord.VoiceChannel):

            perm_sel = manage_components.create_select(
                min_values=1,
                max_values=12,
                placeholder=f"choose the permissions to give the {'user' if isinstance(role_or_user, discord.Member) else 'role'}",
                options=[
                    manage_components.create_select_option(
                        label="view the channel",
                        value="view_channel",
                    ),
                    manage_components.create_select_option(
                        label="manage the channel",
                        value="manage_channels",
                    ),
                    manage_components.create_select_option(
                        label="manage channel permissions",
                        value="manage_permissions",
                    ),
                    manage_components.create_select_option(
                        label="create instant invite",
                        value="create_instant_invite",
                    ),
                    manage_components.create_select_option(
                        label="connect to the channel",
                        value="connect",
                    ),
                    manage_components.create_select_option(
                        label="speak in the channel",
                        value="speak",
                    ),
                    manage_components.create_select_option(
                        label="stream/camera",
                        value="stream",
                    ),
                    manage_components.create_select_option(
                        label="use voice activation",
                        value="use_voice_activation",
                    ),
                    manage_components.create_select_option(
                        label="very important speaker",
                        value="priority_speaker",
                    ),
                    manage_components.create_select_option(
                        label="mute members",
                        value="mute_members",
                    ),
                    manage_components.create_select_option(
                        label="deafen members",
                        value="deafen_members",
                    ),
                    manage_components.create_select_option(
                        label="move members in another channel",
                        value="move_members",
                    ),
                ],
            )
            sel_ar = manage_components.create_actionrow(perm_sel)
            msg = await ctx.send(
                content=f"What Permissions do you want to give the {'user' if isinstance(role_or_user, discord.Member) else 'role'}"
                f"all not selected permissions will be **denied**",
                components=[sel_ar],
            )

            try:
                perms: ComponentContext = await manage_components.wait_for_component(
                    self.bot,
                    components=[sel_ar],
                    timeout=600,
                    check=lambda comp: comp.author.id == ctx.author.id,
                )
                await perms.defer(edit_origin=True)
            except asyncio.TimeoutError:
                sel_ar["components"][0]["disabled"] = True
                await msg.edit(content="Timed out.", components=[sel_ar])
                return

            perm = discord.PermissionOverwrite(
                view_channel=True if "view_channel" in perms.selected_options else False,
                manage_channels=True if "manage_channels" in perms.selected_options else False,
                manage_permissions=True
                if "manage_permissions" in perms.selected_options
                else False,
                create_instant_invite=True
                if "create_instant_invite" in perms.selected_options
                else False,
                connect=True if "connect" in perms.selected_options else False,
                speak=True if "speak" in perms.selected_options else False,
                stream=True if "stream" in perms.selected_options else False,
                use_voice_activation=True
                if "use_voice_activation" in perms.selected_options
                else False,
                priority_speaker=True if "priority_speaker" in perms.selected_options else False,
                mute_members=True if "mute_members" in perms.selected_options else False,
                deafen_members=True if "deafen_members" in perms.selected_options else False,
                move_members=True if "move_members" in perms.selected_options else False,
            )

            sel_ar["components"][0]["disabled"] = True

            await perms.edit_origin(content="Editing channel permissions....", components=[sel_ar])

            perm_overwrite = {
                role_or_user: perm,
            }

            await channel.edit(
                overwrites=perm_overwrite,
                reason=f"User {ctx.author.name} used the channel-permission-edit command!",
            )

    ch_del_opt = [
        {
            "name": "channel",
            "description": "The channel to edit",
            "type": 7,
            "required": True,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="channel",
        name="delete",
        description="deletes a channel",
        options=ch_del_opt,
    )
    async def _channel_delete(
        self, ctx: SlashContext, channel: Union[discord.TextChannel, discord.VoiceChannel]
    ):
        if not ctx.author.guild_permissions.manage_channels:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_channels"])
        await channel.delete(reason=f"User {ctx.author.name} used the channel-delete command!")
        await ctx.send("done", hidden=True)

    cat_cre_opt = [
        {
            "name": "name",
            "description": "the name of the category",
            "type": 3,
            "required": True,
        },
        {
            "name": "position",
            "description": "the position of the category",
            "type": 4,
            "required": False,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="category",
        name="create",
        description="creates a category",
        options=cat_cre_opt,
    )
    async def _category_create(self, ctx: SlashContext, name: str, position: int = None):
        if not ctx.author.guild_permissions.manage_channels:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_channels"])

        else:
            await ctx.guild.create_category(
                name=name,
                position=position + 1 if position is not None else None,
                reason=f"User {ctx.author.name} used the category-create command!",
            )
            await ctx.send("done!", hidden=True)

    cat_edt_opt = [
        {
            "name": "category",
            "description": "The category to delete",
            "type": 7,
            "required": True,
        },
        {
            "name": "name",
            "description": "the new name of the category",
            "type": 3,
            "required": False,
        },
        {
            "name": "position",
            "description": "the new position of the category",
            "type": 4,
            "required": False,
        },
        {
            "name": "role_or_user",
            "description": "if you specify this, you will be able to edit the permissions for a role or a user in that category",
            "type": 9,
            "required": False,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="category",
        name="edit",
        description="edits a category",
        options=cat_edt_opt,
    )
    async def _category_edit(
        self,
        ctx: SlashContext,
        category: discord.CategoryChannel,
        name: str = None,
        position: int = None,
        role_or_user: Union[discord.Member, discord.Role] = None,
    ):
        if not ctx.author.guild_permissions.manage_channels:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_channels"])

        else:
            await ctx.defer(hidden=True)
            if not role_or_user:
                await category.edit(
                    reason=f"User {ctx.author.name} used the category-edit command!",
                    position=position + 1 if position is not None else category.position,
                    name=name if name is not None else category.name,
                )
                await ctx.send("done", hidden=True)
            else:
                text_perm_sel = manage_components.create_select(
                    min_values=1,
                    max_values=14,
                    placeholder=f"set the category text channel perms for the {'user' if isinstance(role_or_user, discord.Member) else 'role'}",
                    options=[
                        manage_components.create_select_option(
                            label="view the channel",
                            value="view_channel",
                        ),
                        manage_components.create_select_option(
                            label="manage the channel",
                            value="manage_channels",
                        ),
                        manage_components.create_select_option(
                            label="manage channel permissions",
                            value="manage_permissions",
                        ),
                        manage_components.create_select_option(
                            label="manage webhooks",
                            value="manage_webhooks",
                        ),
                        manage_components.create_select_option(
                            label="create instant invite",
                            value="create_instant_invite",
                        ),
                        manage_components.create_select_option(
                            label="send messages in the channel",
                            value="send_messages",
                        ),
                        manage_components.create_select_option(
                            label="embed links in messages",
                            value="embed_links",
                        ),
                        manage_components.create_select_option(
                            label="attach files to messages",
                            value="attach_files",
                        ),
                        manage_components.create_select_option(
                            label="add reactions to messages",
                            value="add_reactions",
                        ),
                        manage_components.create_select_option(
                            label="use external emojis in messages",
                            value="use_external_emojis",
                        ),
                        manage_components.create_select_option(
                            label="mention @everyone",
                            value="mention_everyone",
                        ),
                        manage_components.create_select_option(
                            label="manage messages",
                            value="manage_messages",
                        ),
                        manage_components.create_select_option(
                            label="read message history",
                            value="read_message_history",
                        ),
                        manage_components.create_select_option(
                            label="send tts messages",
                            value="send_tts_messages",
                        ),
                    ],
                )
                text_sel_ar = manage_components.create_actionrow(text_perm_sel)
                msg = await ctx.send(
                    content=f"What Permissions do you want to give the {'user' if isinstance(role_or_user, discord.Member) else 'role'} in the category?"
                    f"all not selected permissions will be **denied**",
                    components=[text_sel_ar],
                )

                try:
                    text_perms: ComponentContext = await manage_components.wait_for_component(
                        self.bot,
                        components=[text_sel_ar],
                        timeout=600,
                        check=lambda comp: comp.author.id == ctx.author.id,
                    )
                    await text_perms.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    text_sel_ar["components"][0]["disabled"] = True
                    await msg.edit(content="Timed out.", components=[text_sel_ar])
                    return

                voice_perm_sel = manage_components.create_select(
                    min_values=1,
                    max_values=8,
                    placeholder=f"set the category voice channel perms for the {'user' if isinstance(role_or_user, discord.Member) else 'role'}",
                    options=[
                        manage_components.create_select_option(
                            label="connect to the channel",
                            value="connect",
                        ),
                        manage_components.create_select_option(
                            label="speak in the channel",
                            value="speak",
                        ),
                        manage_components.create_select_option(
                            label="stream/camera",
                            value="stream",
                        ),
                        manage_components.create_select_option(
                            label="use voice activation",
                            value="use_voice_activation",
                        ),
                        manage_components.create_select_option(
                            label="very important speaker",
                            value="priority_speaker",
                        ),
                        manage_components.create_select_option(
                            label="mute members",
                            value="mute_members",
                        ),
                        manage_components.create_select_option(
                            label="deafen members",
                            value="deafen_members",
                        ),
                        manage_components.create_select_option(
                            label="move members in another channel",
                            value="move_members",
                        ),
                    ],
                )
                voice_sel_ar = manage_components.create_actionrow(voice_perm_sel)
                await text_perms.edit_origin(
                    content=f"What Permissions do you want to give the {'user' if isinstance(role_or_user, discord.Member) else 'role'} in the category?"
                    f"all not selected permissions will be **denied**",
                    components=[voice_sel_ar],
                )

                try:
                    voice_perms: ComponentContext = await manage_components.wait_for_component(
                        self.bot,
                        components=[voice_sel_ar],
                        timeout=600,
                        check=lambda comp: comp.author.id == ctx.author.id,
                    )
                    await voice_perms.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    voice_sel_ar["components"][0]["disabled"] = True
                    await text_perms.origin_message.edit(
                        content="Timed out.", components=[voice_sel_ar]
                    )
                    return

                allperms = discord.PermissionOverwrite(
                    view_channel=True if "view_channel" in text_perms.selected_options else False,
                    manage_channels=True
                    if "manage_channels" in text_perms.selected_options
                    else False,
                    manage_permissions=True
                    if "manage_permissions" in text_perms.selected_options
                    else False,
                    manage_webhooks=True
                    if "manage_webhooks" in text_perms.selected_options
                    else False,
                    create_instant_invite=True
                    if "create_instant_invite" in text_perms.selected_options
                    else False,
                    send_messages=True if "send_messages" in text_perms.selected_options else False,
                    embed_links=True if "embed_links" in text_perms.selected_options else False,
                    attach_files=True if "attach_files" in text_perms.selected_options else False,
                    add_reactions=True if "add_reactions" in text_perms.selected_options else False,
                    use_external_emojis=True
                    if "use_external_emojis" in text_perms.selected_options
                    else False,
                    mention_everyone=True
                    if "mention_everyone" in text_perms.selected_options
                    else False,
                    manage_messages=True
                    if "manage_messages" in text_perms.selected_options
                    else False,
                    read_message_history=True
                    if "read_message_history" in text_perms.selected_options
                    else False,
                    send_tts_messages=True
                    if "send_tts_messages" in text_perms.selected_options
                    else False,
                    connect=True if "connect" in voice_perms.selected_options else False,
                    speak=True if "speak" in voice_perms.selected_options else False,
                    stream=True if "stream" in voice_perms.selected_options else False,
                    use_voice_activation=True
                    if "use_voice_activation" in voice_perms.selected_options
                    else False,
                    priority_speaker=True
                    if "priority_speaker" in voice_perms.selected_options
                    else False,
                    mute_members=True if "mute_members" in voice_perms.selected_options else False,
                    deafen_members=True
                    if "deafen_members" in voice_perms.selected_options
                    else False,
                    move_members=True if "move_members" in voice_perms.selected_options else False,
                )

                voice_sel_ar["components"][0]["disabled"] = True

                all_ovwerite = {role_or_user: allperms}

                await category.edit(
                    reason=f"User {ctx.author.name} used the category-edit command!",
                    position=position + 1 if position is not None else category.position,
                    name=name if name is not None else category.name,
                    overwrites=all_ovwerite,
                )
                await voice_perms.edit_origin(content="Done!", components=[voice_sel_ar])

    cat_del_opt = [
        {
            "name": "category",
            "description": "The category to delete",
            "type": 7,
            "required": True,
        },
    ]

    @cog_ext.cog_subcommand(
        base="server",
        subcommand_group="category",
        name="delete",
        description="deletes a category",
        options=cat_del_opt,
    )
    async def _cat_delete(self, ctx: SlashContext, category: discord.CategoryChannel):
        if not ctx.author.guild_permissions.manage_channels:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_channels"])

        else:
            await category.delete(
                reason=f"User {ctx.author.name} used the category-delete command!"
            )
            await ctx.send("done!", hidden=True)


def setup(bot: AutoShardedBot):
    bot.add_cog(ServerUtils(bot))
