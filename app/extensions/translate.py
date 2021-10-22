import hikari
from hikari.embeds import Embed
import lightbulb
from deep_translator import GoogleTranslator
from lightbulb import slash_commands
from app import *



class Translate(slash_commands.SlashCommand):
    description = 'Use this command to translate from any language for more than 100 language'

    language: str = slash_commands.Option('Put here shortcut code for the language that you want to user', required=True)
    text: str = slash_commands.Option('Type anything here to translate it', required=True)

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]


    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        if ctx.options.language not in config['langs']:
            return await ctx.respond(f'There are no language named `{ctx.options.language}`!')
        trans = GoogleTranslator(target=f'{ctx.options.language}').translate(ctx.options.text)
        embed = Embed(color=0x2C3434, description=trans)
        await ctx.respond(embed=embed)
        words = len(str(ctx.options.text).split())
        if get_translated_words := translated_words.find_one({'guild_id': f'{ctx.get_guild().id}'}):
            new_count = get_translated_words['translated_words'] + words
            data = {
                'guild_id': f'{ctx.get_guild().id}',
                'translated_words': new_count
            }
            translated_words.update_one({'guild_id': f'{ctx.get_guild().id}'}, {'$set': data})
        else:
            data = {
                'guild_id': f'{ctx.get_guild().id}',
                'translated_words': words
            }
            translated_words.insert_one(data)


def load(bot: Bot) -> None:
    bot.add_slash_command(Translate)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Translate')