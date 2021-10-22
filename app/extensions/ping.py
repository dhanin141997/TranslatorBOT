import lightbulb
from lightbulb import slash_commands
from datetime import datetime as dt
from app import *



class Ping(slash_commands.SlashCommand):
    description = 'Shows bot\'s ping'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        start = dt.timestamp(dt.now())
        await ctx.respond(f'...')
        await ctx.edit_response(
            f'Discord API: {ctx.bot.heartbeat_latency * 1_000:,.0f}\nLatency: {round((dt.timestamp(dt.now()) - start) * 1000)}'
        )


def load(bot: Bot) -> None:
    bot.add_slash_command(Ping)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Ping')
