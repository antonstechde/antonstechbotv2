from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission

# Everyone who is in this config can do many Evil Things so think about who you should put in this config
# For Example:


def get_admin_permissions():
    adminperms = {
        723220208772186156: [
            create_permission(708275751816003615, SlashCommandPermissionType.USER, True),  # Ed_Vraz
            create_permission(450415578654441486, SlashCommandPermissionType.USER, True),  # Ole
            create_permission(327906969971326976, SlashCommandPermissionType.USER, True),  # anton
        ]
    }
    return adminperms
