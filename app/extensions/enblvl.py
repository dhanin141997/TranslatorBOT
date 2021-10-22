import hikari
from hikari.messages import MessageFlag
import lightbulb
from lightbulb import slash_commands
from app import *



def guild_owner(ctx: slash_commands.SlashCommandContext) -> bool:
        return ctx.member.id == ctx.get_guild().owner_id


class Enblvl(slash_commands.SlashCommand):
    description = 'Use this command to enable the leveling for this server (Owner Only)'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
        lightbulb.Check(guild_owner)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        guild_lvl = dislvl.find_one({'guild_id': f'{ctx.get_guild().id}'})

        if not guild_lvl:
            await ctx.respond(f'Leveling already enabled', flags=MessageFlag.EPHEMERAL)
        else:
            dislvl.delete_one({'guild_id': f'{ctx.get_guild().id}'})
            await ctx.respond('Leveling is enabled now', flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: Bot) -> None:
    bot.add_slash_command(Enblvl)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Enblvl')