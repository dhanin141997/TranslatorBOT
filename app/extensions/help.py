import hikari
from hikari.messages import MessageFlag
import lightbulb
from lightbulb import slash_commands
from app import *



class Help(slash_commands.SlashCommand):
    description = 'Help command'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.respond(
            'Type `/` that will show you all the commands are available or join discord.gg/XKH8BkZJXN',
            flags=MessageFlag.EPHEMERAL
        )


def load(bot: Bot) -> None:
    bot.add_slash_command(Help)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Help')