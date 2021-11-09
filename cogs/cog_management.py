import asyncio
import os
import time

import discord
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import SlashCommandPermissionType, ButtonStyle
from discord_slash.utils import manage_components
from discord_slash.utils.manage_commands import create_permission
from discord_slash.utils.manage_components import wait_for_component

from .basicerror import basicerror
from config.adminconfig import get_admin_permissions
from utils import utils
from discord.ext import commands


class cog_management(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="cog", description="lets you reload, load and unload cogs", guild_ids=[792862721556480031])
    async def _cog_management(self, ctx: SlashContext):
        await ctx.defer(hidden=False)
        options = [
            manage_components.create_button(
                label="RELOAD", style=ButtonStyle.red, custom_id="reload"
            ),
            manage_components.create_button(
                label="UNLOAD", style=ButtonStyle.red, custom_id="unload"
            ),
            manage_components.create_button(
                label="LOAD", style=ButtonStyle.red, custom_id="load"
            )
        ]
        options_actionrow = manage_components.create_actionrow(*options)
        message = await ctx.send(
            f"What d0 u wanna 2 do m8? (timeout: 60 seconds)",
            hidden=False,
            components=[
                options_actionrow
            ],
        )
        try:
            buttons: ComponentContext = await wait_for_component(self.bot, components=[options_actionrow],
                                                                 timeout=60,
                                                                 check=lambda msg: ctx.author.id == msg.author.id)
        except asyncio.TimeoutError:
            for i in range(3):
                options_actionrow["components"][i]["disabled"] = True
            await message.edit(content="Timed out.", components=[options_actionrow])  # Disable the Buttons
            return

        if buttons.component_id == "reload":
            unload_button = [
                manage_components.create_button(
                    label="Reload all Cogs", style=ButtonStyle.red, custom_id="rl all"
                ),
                manage_components.create_button(
                    label="Reload specific Cog", style=ButtonStyle.red, custom_id="rl spec"
                )
            ]
            rl_actionrow = manage_components.create_actionrow(*unload_button)
            await buttons.edit_origin(
                content="Do u wanna reload all or a specific Cog?",
                hidden=False,
                components=[rl_actionrow]

            )
            unload_button_ctx: ComponentContext = await manage_components.wait_for_component(
                self.bot, components=rl_actionrow, check=lambda msg: ctx.author.id == msg.author.id
            )
            if unload_button_ctx.component_id == "rl all":
                await unload_button_ctx.edit_origin(content="reloading...")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py") and filename not in ["basicerror.py"]:
                        try:
                            utils.LOGGER.info(f"Reloading {filename}")
                            self.bot.reload_extension(f"cogs.{filename[:-3]}")
                        except Exception as e:
                            await unload_button_ctx.send(content=f"Failed to reload {filename[:-3]}")
                            return
                await unload_button_ctx.origin_message.edit(content="Successfully reloaded all Cogs.", components=[])

            elif unload_button_ctx.component_id == "rl spec":
                await unload_button_ctx.edit_origin(
                    content="Please provide the Name of the Cog that should be reloaded!")
                try:
                    answer = await self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id,
                                                     timeout=600)
                except asyncio.TimeoutError:
                    await buttons.origin_message.edit("Timed out, process canceled.")
                    return
                cogname = str(answer.content)
                try:
                    self.bot.reload_extension(f"cogs.{cogname}")
                    await answer.delete()
                    await unload_button_ctx.origin_message.edit(content=f"Successfully reloaded {cogname}.", components=[])
                except:
                    await unload_button_ctx.origin_message.edit(content=f"Failed to reload {cogname}.", components=[])
                    return

        elif buttons.component_id == "load":
            unload_button = [
                manage_components.create_button(
                    label="Load all Cogs", style=ButtonStyle.red, custom_id="l all"
                ),
                manage_components.create_button(
                    label="Load specific Cog", style=ButtonStyle.red, custom_id="l spec"
                )
            ]
            rl_actionrow = manage_components.create_actionrow(*unload_button)
            await buttons.edit_origin(
                content="Do u wanna load all or a specific Cog?",
                hidden=False,
                components=[rl_actionrow]

            )
            unload_button_ctx: ComponentContext = await manage_components.wait_for_component(
                self.bot, components=rl_actionrow, check=lambda msg: ctx.author.id == msg.author.id
            )
            if unload_button_ctx.component_id == "l all":
                await unload_button_ctx.edit_origin(content="loading...")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py") and filename not in ["basicerror.py", "cog_management.py"]:
                        try:
                            utils.LOGGER.info(f"loading {filename}")
                            self.bot.load_extension(f"cogs.{filename[:-3]}")
                        except Exception as e:
                            await unload_button_ctx.send(content=f"This command trys to load **all** cogs which is not working when only a single cog is already loaded. So only use this function if you unloaded all before")
                            return
                await unload_button_ctx.origin_message.edit(content="Successfully reloaded all Cogs.", components=[])

            elif unload_button_ctx.component_id == "l spec":
                await unload_button_ctx.edit_origin(
                    content="Please provide the Name of the Cog that should be loaded!")
                try:
                    answer = await self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id,
                                                     timeout=600)
                except asyncio.TimeoutError:
                    await buttons.origin_message.edit("Timed out, process canceled.")
                    return
                cogname = str(answer.content)
                try:
                    self.bot.load_extension(f"cogs.{cogname}")
                    await answer.delete()
                    await unload_button_ctx.origin_message.edit(content=f"Successfully loaded {cogname}.",
                                                                components=[])
                except:
                    await unload_button_ctx.origin_message.edit(content=f"Failed to load {cogname}.", components=[])
                    return
        elif buttons.component_id == "unload":
            unload_button = [
                manage_components.create_button(
                    label="Unload all Cogs", style=ButtonStyle.red, custom_id="u all"
                ),
                manage_components.create_button(
                    label="Unload specific Cog", style=ButtonStyle.red, custom_id="u spec"
                )
            ]
            rl_actionrow = manage_components.create_actionrow(*unload_button)
            await buttons.edit_origin(
                content="Do u wanna unload all or a specific Cog?",
                hidden=False,
                components=[rl_actionrow]

            )
            unload_button_ctx: ComponentContext = await manage_components.wait_for_component(
                self.bot, components=rl_actionrow, check=lambda msg: ctx.author.id == msg.author.id
            )
            if unload_button_ctx.component_id == "u all":
                await unload_button_ctx.edit_origin(content="unloading...")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py") and filename not in ["basicerror.py", "cog_management.py"]:
                        try:
                            utils.LOGGER.info(f"unloading {filename}")
                            self.bot.unload_extension(f"cogs.{filename[:-3]}")
                        except Exception as e:
                            await unload_button_ctx.send(
                                content=f"Failed unloading {filename}")
                            return
                await unload_button_ctx.origin_message.edit(content="Successfully unloaded all Cogs.", components=[])

            elif unload_button_ctx.component_id == "u spec":
                await unload_button_ctx.edit_origin(
                    content="Please provide the Name of the Cog that should be unloaded!")
                try:
                    answer = await self.bot.wait_for("message", check=lambda msg: msg.author.id == buttons.author.id,
                                                     timeout=600)
                except asyncio.TimeoutError:
                    await buttons.origin_message.edit("Timed out, process canceled.")
                    return
                cogname = str(answer.content)
                try:
                    self.bot.unload_extension(f"cogs.{cogname}")
                    await answer.delete()
                    await unload_button_ctx.origin_message.edit(content=f"Successfully unloaded {cogname}.",
                                                              components=[])
                except:
                    await unload_button_ctx.origin_message.edit(content=f"Failed to unload {cogname}.", components=[])
                    return


def setup(bot: Bot):
    bot.add_cog(cog_management(bot))
