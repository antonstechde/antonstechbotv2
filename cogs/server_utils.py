import asyncio
import discord
import re
from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext, ButtonStyle, ComponentContext
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import wait_for_component, create_select_option
from utils import utils, punishments


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
            min_values=1, max_values=18,
            options=[
                create_select_option(
                    label="add reactions to messages",
                    value="add_reactions",
                ),
                create_select_option(
                    label="attach files to messages",
                    value="attach_files",
                ),
                create_select_option(
                    label="ban members",
                    value="ban_members",
                ),
                create_select_option(
                    label="change own nickname",
                    value="change_nickname",
                ),
                create_select_option(
                    label="connect to voice channels",
                    value="connect",
                ),
                create_select_option(
                    label="create instant invite to a channel",
                    value="create_instant_invite",
                ),
                create_select_option(
                    label="deafen other members in voice channels",
                    value="deafen_members",
                ),
                create_select_option(
                    label="embed links in channels",
                    value="embed_links",
                ),
                create_select_option(
                    label="send external emojis",
                    value="external_emojis",
                ),
                create_select_option(
                    label="kick members",
                    value="kick_members",
                ),
                create_select_option(
                    label="manage channels on the server",
                    value="manage_channels",
                ),
                create_select_option(
                    label="manage emojis of the server",
                    value="manage_emojis",
                ),
                create_select_option(
                    label="manage guild",
                    value="manage_guild",
                ),
                create_select_option(
                    label="manage messages",
                    value="manage_messages",
                ),
                create_select_option(
                    label="manage all nicknames",
                    value="manage_nicknames",
                ),
                create_select_option(
                    label="manage the permission of roles",
                    value="manage_permissions",
                ),
                create_select_option(
                    label="manage roles and their permissions",
                    value="manage_roles",
                ),
                create_select_option(
                    label="manage webhooks",
                    value="manage_webhooks"
                ),
            ],
        )
        selrow = manage_components.create_actionrow(sel)
        await ctx.edit_origin(
            content="Please choose the permissions you want to assign to the role (1/2)",
            components=[selrow]
        )

        try:
            firstperms = await wait_for_component(self.bot, components=[selrow], timeout=600,
                                                  check=lambda msg: msg.author.id == ctx.author.id)
            await firstperms.defer(edit_origin=True)
        except asyncio.TimeoutError:
            selrow["components"][0]["disabled"] = True
            await ctx.origin_message.edit("Timed out.", components=[selrow])
            return

        roleperm.add_reactions = True if "add_reactions" in firstperms.selected_options else False
        roleperm.attach_files = True if "attach_files" in firstperms.selected_options else False
        roleperm.ban_members = True if "ban_members" in firstperms.selected_options else False
        roleperm.change_nickname = True if "change_nickname" in firstperms.selected_options else False
        roleperm.connect = True if "connect" in firstperms.selected_options else False
        roleperm.create_instant_invite = True if "create_instant_invite" in firstperms.selected_options else False
        roleperm.deafen_members = True if "deafen_members" in firstperms.selected_options else False
        roleperm.embed_links = True if "embed_links" in firstperms.selected_options else False
        roleperm.external_emojis = True if "external_emojis" in firstperms.selected_options else False
        roleperm.kick_members = True if "kick_members" in firstperms.selected_options else False
        roleperm.manage_channels = True if "manage_channels" in firstperms.selected_options else False
        roleperm.manage_emojis = True if "manage_emojis" in firstperms.selected_options else False
        roleperm.manage_guild = True if "manage_guild" in firstperms.selected_options else False
        roleperm.manage_messages = True if "manage_messages" in firstperms.selected_options else False
        roleperm.manage_nicknames = True if "manage_nicknames" in firstperms.selected_options else False
        roleperm.manage_permissions = True if "manage_permissions" in firstperms.selected_options else False
        roleperm.manage_roles = True if "manage_roles" in firstperms.selected_options else False
        roleperm.manage_webhooks = True if "manage_webhooks" in firstperms.selected_options else False

        sel2 = manage_components.create_select(
            placeholder="Choose the permissions you want for your role (2/2)",
            max_values=17, min_values=1,
            options=[
                create_select_option(
                    label="mention everyone in a message",
                    value="mention_everyone",
                ),
                create_select_option(
                    label="move members across voice channels",
                    value="move_members",
                ),
                create_select_option(
                    label="mute members in voice channels",
                    value="mute_members",
                ),
                create_select_option(
                    label="priority speaker",
                    value="priority_speaker",
                ),
                create_select_option(
                    label="read message history in channels",
                    value="read_message_history",
                ),
                create_select_option(
                    label="read all messages in channels",
                    value="read_messages",
                ),
                create_select_option(
                    label="request to speak in stage channels",
                    value="request_to_speak",
                ),
                create_select_option(
                    label="send messages in channels",
                    value="send_messages",
                ),
                create_select_option(
                    label="send TTS messages in channels",
                    value="send_tts_messages",
                ),
                create_select_option(
                    label="speak in voice channels",
                    value="speak",
                ),
                create_select_option(
                    label="stream in voice channels",
                    value="stream",
                ),
                create_select_option(
                    label="use external emojis",
                    value="use_external_emojis",
                ),
                create_select_option(
                    label="use slash commands in channels",
                    value="use_slash_commands",
                ),
                create_select_option(
                    label="use voice activation in voice channels (else only push-to-talk)",
                    value="use_voice_activation",
                ),
                create_select_option(
                    label="view the audit-log",
                    value="view_audit_log",
                ),
                create_select_option(
                    label="view channels",
                    value="view_channel",
                ),
                create_select_option(
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
            secondperms = await wait_for_component(self.bot, components=[sel2row], timeout=600,
                                                   check=lambda msg: msg.author.id == ctx.author.id)
            await secondperms.defer(edit_origin=True)
        except asyncio.TimeoutError:
            sel2row["components"][0]["disabled"] = True
            await firstperms.origin_message.edit("Timed out.", components=[sel2row])
            return

        roleperm.mention_everyone = True if "mention_everyone" in secondperms.selected_options else False
        roleperm.move_members = True if "move_members" in secondperms.selected_options else False
        roleperm.mute_members = True if "mute_members" in secondperms.selected_options else False
        roleperm.priority_speaker = True if "priority_speaker" in secondperms.selected_options else False
        roleperm.read_message_history = True if "read_message_history" in secondperms.selected_options else False
        roleperm.read_messages = True if "read_messages" in secondperms.selected_options else False
        roleperm.request_to_speak = True if "request_to_speak" in secondperms.selected_options else False
        roleperm.send_messages = True if "send_messages" in secondperms.selected_options else False
        roleperm.send_tts_messages = True if "send_tts_messages" in secondperms.selected_options else False
        roleperm.speak = True if "speak" in secondperms.selected_options else False
        roleperm.stream = True if "stream" in secondperms.selected_options else False
        roleperm.use_external_emojis = True if "use_external_emojis" in secondperms.selected_options else False
        roleperm.use_slash_commands = True if "use_slash_commands" in secondperms.selected_options else False
        roleperm.use_voice_activation = True if "use_voice_activation" in secondperms.selected_options else False
        roleperm.view_audit_log = True if "view_audit_log" in secondperms.selected_options else False
        roleperm.view_channel = True if "view_channel" in secondperms.selected_options else False
        roleperm.view_guild_insights = True if "view_guild_insights" in secondperms.selected_options else False

        return roleperm, sel2row, secondperms

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
                and not ctx.author.guild_permissions.kick_members
                and not ctx.author.guild_permissions.manage_messages):
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
            await buttons.defer(edit_origin=True)
        except asyncio.TimeoutError:
            for i in range(2):
                user_buttons_actionrow1["components"][i]["disabled"] = True
                user_buttons_actionrow2["components"][i]["disabled"] = True
            user_buttons_actionrow3["components"][0]["disabled"] = True
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
                    times_ctx: ComponentContext = await manage_components.wait_for_component(
                        self.bot, components=[times1_row, times2_row, times3_row],
                        check=lambda msg: msg.author.id == mute_btn_ctx.author.id, timeout=180,
                    )
                    await times_ctx.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    for i in range(4):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.origin_message.edit(
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
                    await times_ctx.defer(edit_origin=True)
                except asyncio.TimeoutError:
                    for i in range(5):
                        times1_row["components"][i]["disabled"] = True
                        times2_row["components"][i]["disabled"] = True
                        times3_row["components"][i]["disabled"] = True
                        times4_row["components"][i]["disabled"] = True
                        times5_row["components"][i]["disabled"] = True
                    await mute_btn_ctx.origin_message.edit(
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
                a = await self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id,
                                            timeout=600)
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
                a = await self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id,
                                            timeout=600)
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
                a = await self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id,
                                            timeout=600)
            except asyncio.TimeoutError:
                await buttons.origin_message.edit("Timed out, process canceled.")
                return
            reason = str(a.content)
            await a.delete()
            await buttons.origin_message.delete()
            await punishments.ban(ctx, user, reason)

    @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="unban", description="unbans a user")
    async def _unban(self, ctx: SlashContext, user_id: str,
                     reason: str):  # in theory discord-slash should automatically create options for that
        user_id = int(user_id)
        user: discord.User = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user=user, reason=reason)
        await ctx.send(f"unbanned {user.mention}!")

    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="un-punish", description="un-punishes a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="add-role", description="adds a role to a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="remove-role", description="removes a role from a user")

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

    @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="create", description="creates a role",
                            options=rcre_opt)
    async def _create_role(self, ctx: SlashContext, name: str, color: str, hoist: bool = False,
                           mentionable: bool = False):
        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.errors.MissingPermissions(missing_perms=["manage_roles"])
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)  # check if color is hex
        if not match:
            raise discord.ext.commands.BadArgument("color is not a hex-color code")
        hexval = color.lstrip("#")
        rgbval = tuple(bytes.fromhex(hexval))
        await ctx.defer(hidden=False)

        roleperm = discord.Permissions().none()
        color = discord.Colour.from_rgb(r=rgbval[0], g=rgbval[1], b=rgbval[2])

        anypermbutton = [
            manage_components.create_button(
                label="Yes", style=ButtonStyle.green, custom_id="yes"
            ),
            manage_components.create_button(
                label="No", style=ButtonStyle.red, custom_id="no"
            )
        ]

        adminbutton = [
            manage_components.create_button(
                label="Yes", style=ButtonStyle.green, custom_id="yes"
            ),
            manage_components.create_button(
                label="No", style=ButtonStyle.red, custom_id="no"
            ),
        ]
        any_ar = manage_components.create_actionrow(*anypermbutton)
        adm_ar = manage_components.create_actionrow(*adminbutton)

        ask = await ctx.send(
            "Do you want to have any Permission enabled on your role?",
            components=[any_ar]
        )

        try:
            answer: ComponentContext = await wait_for_component(self.bot, components=[any_ar],
                                                                timeout=600,
                                                                check=lambda msg: ctx.author.id == msg.author.id)
            await answer.defer(edit_origin=True)
        except asyncio.TimeoutError:
            for i in range(2):
                any_ar["components"][i]["disabled"] = True
            await ask.edit(
                content="Timed out.", components=[any_ar]
            )
            return

        if answer.component_id == "no":
            for i in range(2):
                any_ar["components"][i]["disabled"] = True
            await answer.edit_origin(
                content=f"creating role '{name}' with the color #{hexval} and no permissions....",
                components=[any_ar]
            )
            await ctx.guild.create_role(name=name, color=color, permissions=roleperm, hoist=hoist,
                                        mentionable=mentionable)
            await ctx.channel.send("Done")
            return

        else:
            pass

        await answer.edit_origin(
            content="Do you want the role to have administrator-permissions?",
            components=[adm_ar]
        )
        try:
            admin: ComponentContext = await wait_for_component(self.bot, components=[adm_ar], timeout=600,
                                                               check=lambda msg: msg.author.id == ctx.author.id)
            await admin.defer(edit_origin=True)
        except asyncio.TimeoutError:
            for i in range(2):
                adm_ar["components"][i]["disabled"] = True
            await ask.edit(
                content="Timed out.", components=[adm_ar]
            )
            return

        if admin.component_id == "yes":
            roleperm.administrator = True
            for i in range(2):
                adm_ar["components"][i]["disabled"] = True
            await admin.edit_origin(
                content=f"creating role '{name}' with the color #{hexval} and administrator permissions....",
                components=[adm_ar]
            )
            await ctx.guild.create_role(name=name, color=color, permissions=roleperm, hoist=hoist,
                                        mentionable=mentionable)
            await ctx.channel.send("Done")
            return

        else:
            try:
                roleperm, sel2row, secondperms = await self._get_role_permissions(ctx=admin, roleperm=roleperm)
            except ValueError:  # on timeout no values returned, just do nothing then
                return

        sel2row["components"][0]["disabled"] = True
        await secondperms.edit_origin(
            content=f"Role '{name}' with color #{hexval} and your custom permissions, which have the value {roleperm.value}, is being created",
            components=[sel2row]
        ),
        await ctx.guild.create_role(name=name, color=color, permissions=roleperm, hoist=hoist, mentionable=mentionable)

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

    @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="edit", description="edits a role",
                            options=redt_opt)
    async def _role_edit(self, ctx: SlashContext, role: discord.Role, name: str = None, color: str = None,
                         hoist: bool = None, mentionable: bool = None):

        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.errors.MissingPermissions(missing_perms=["manage_roles"])

        if not name:
            name = role.name

        if not hoist:
            hoist = role.hoist

        if not mentionable:
            mentionable = role.mentionable

        if color:
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)  # check if color is hex
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
                label="Yes", style=ButtonStyle.green,
                custom_id="yes",
            ),
            manage_components.create_button(
                label="No", style=ButtonStyle.red,
                custom_id="no",
            ),
        ]

        perm_ar = manage_components.create_actionrow(*perm_edt)

        msg = await ctx.send("Do you want to edit the permissions of the role?", components=[perm_ar])

        try:
            perm: ComponentContext = await wait_for_component(self.bot, components=[perm_ar], timeout=600,
                                                              check= lambda m: m.author.id == ctx.author.id)
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
                content="editing the role without changing permissions?",
                components=[perm_ar]
            )
            await role.edit(permissions=roleperm, name=name, hoist=hoist, mentionable=mentionable, colour=color)
            await perm.origin_message.edit(content="Done")



    rdel_opt = [
        {
            "name": "role",
            "description": "the role to delete",
            "required": True,
            "type": 8,
        }
    ]

    @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="delete", description="deletes a role",
                            options=rdel_opt)
    async def _delete_role(self, ctx: SlashContext, role: discord.Role):
        if not ctx.author.guild_permissions.manage_roles:
            raise discord.ext.commands.MissingPermissions(missing_perms=["manage_roles"])
        await role.delete()
        await ctx.send("role has been deleted")

    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="create", description="creates a channel")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="edit", description="edits a channel") # not sure about that one
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="delete", description="deletes a channel")

    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="create", description="creates a category")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="edit", description="edits a category") # not sure about that one
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="delete", description="deletes a category")


def setup(bot: AutoShardedBot):
    bot.add_cog(ServerUtils(bot))
