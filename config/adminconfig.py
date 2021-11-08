from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType


# Everyone who is in this config can do many Evil Things so think about who you should put in this config
# For Example:

def get_admin_permissions():
    adminperms = {
        723220208772186156: [  # only on our Discord Server
            create_permission(782026258921553933, SlashCommandPermissionType.ROLE, True),  # Mod role
            create_permission(907261618088443914, SlashCommandPermissionType.ROLE, True)  # Developer role
        ],
        792862721556480031: [
            create_permission(327906969971326976, SlashCommandPermissionType.USER, True)  # Me on my testing server
        ]
    }
    return adminperms
