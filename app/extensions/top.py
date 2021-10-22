import hikari
from hikari.embeds import Embed
import lightbulb
from lightbulb import slash_commands
from app import *



class Top(slash_commands.SlashCommandGroup):
    description = 'Top levels and coins'



@Top.subcommand()
class Levels(slash_commands.SlashSubCommand):
    description = 'Shows the top users by levels'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        embed = Embed(color=0x2C3434)
        embed.set_author(name='Top users by exp', icon=ctx.author.avatar_url)
        usrs = usr_lvl.find().sort('exp', -1).limit(5)
        for num, usr in enumerate(usrs):
            if num == 5: break
            fetch_usr = await ctx.bot.rest.fetch_user(int(usr['user_id']))
            embed.add_field(
                name=f'{num+1}. {fetch_usr.username}',
                value=f'**Exp: `{usr["exp"]:,}`, Level: `{usr["level"]:,}`**',
                inline=False
            )
        await ctx.respond(embed=embed)



@Top.subcommand()
class Coins(slash_commands.SlashSubCommand):
    description = 'Shows the top users by coins'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        embed = Embed(color=0x2C3434)
        embed.set_author(name='Top users by coins', icon=ctx.author.avatar_url)
        usrs = usr_card.find().sort('coins', -1).limit(5)
        for num, usr in enumerate(usrs):
            if num == 5: break
            fetch_usr = await ctx.bot.rest.fetch_user(int(usr['user_id']))
            embed.add_field(
                name=f'{num+1}. {fetch_usr.username}',
                value=f'**Coins: `{usr["coins"]:,}`, RP\'s: `{usr["rps"]:,}`**',
                inline=False
            )
        await ctx.respond(embed=embed)



def load(bot: Bot) -> None:
    bot.add_slash_command(Top)

def unload(bot: Bot) -> None:
    bot.add_slash_command('Top')