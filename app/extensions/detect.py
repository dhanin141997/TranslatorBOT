import hikari
import lightbulb
from langdetect import detect, DetectorFactory
from lightbulb import slash_commands
from app import *

DetectorFactory.seed = 0



class Detect(slash_commands.SlashCommand):
    description = 'Use this command to the name of the language you are using'

    text: str = slash_commands.Option('Type any text to detect it language', required=True)

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        resault = detect(ctx.options.text)
        await ctx.respond(resault)


def load(bot: Bot) -> None:
    bot.add_slash_command(Detect)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Detect')