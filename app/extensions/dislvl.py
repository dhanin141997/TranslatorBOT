import hikari
from hikari.messages import MessageFlag
import lightbulb
from lightbulb import slash_commands
from app import *



class Dislvl(slash_commands.SlashCommand):
    description = 'Use this command to disable the leveling for this server (Owner Only)'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
        lightbulb.Check(guild_owner)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        guild_lvl = dislvl.find_one({'guild_id': f'{ctx.get_guild().id}'})

        if guild_lvl:
            await ctx.respond(f'Leveling already disabled', flags=MessageFlag.EPHEMERAL)
        else:
            data = {
                'guild_id': f'{ctx.get_guild().id}'
            }
            dislvl.insert_one(data)
            await ctx.respond('Leveling is disabled now', flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: Bot) -> None:
    bot.add_slash_command(Dislvl)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Dislvl')