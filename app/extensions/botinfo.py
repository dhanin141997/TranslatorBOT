import hikari
from hikari.embeds import Embed
import lightbulb
from lightbulb import slash_commands
from app import *



class BotInfo(slash_commands.SlashCommand):
    description = 'Use this command to show some information about me'

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        embed = Embed(color=0x2C3434)
        embed.add_field(
            name='Guilds',
            value=f'{len(ctx.bot.cache.get_guilds_view())}',
            inline=True
        )
        # members = []
        # for guild in ctx.bot.cache.get_guilds_view():
        #     guild = await ctx.bot.rest.fetch_guild(guild)
        #     for member in guild.get_members():
        #         members.append(member)
        # members = len(members)
        embed.add_field(
            name='Users',
            value=f'{len(ctx.bot.cache.get_members_view())}',
            inline=True
        )
        embed.add_field(
            name='Version',
            value=f'{version}',
            inline=True
        )
        embed.add_field(
            name='Prefix',
            value='`/`',
            inline=True
        )
        embed.add_field(
            name='Support',
            value='[Click](https://discord.gg/XKH8BkZJXN)',
            inline=True
        )
        embed.add_field(
            name='Invite',
            value='[Click](https://discord.com/api/oauth2/authorize?client_id=853198721847132210&permissions=380104985664&scope=bot%20applications.commands)',
            inline=True
        )
        await ctx.respond(embed=embed)


def load(bot: Bot) -> None:
    bot.add_slash_command(BotInfo)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('BotInfo')