import hikari
from hikari.messages import MessageFlag
from hikari.interactions.base_interactions import ResponseType
import lightbulb
from lightbulb import slash_commands
from app import *



class MultiTrans(slash_commands.SlashCommand):
    description = 'Use this command to set auto translate channel with two languages (Adminstrator Only)'

    channel: hikari.TextableChannel = slash_commands.Option(
        'Pick a channel to set it as auto translate channel with two languages',
        required=True
    )
    language1: str = slash_commands.Option(
        'Enter to shortcut code for the language that you want to set for auto translate channel',
        required=True
    )
    language2: str = slash_commands.Option(
        'Enter to shortcut code for the language that you want to set for auto translate channel',
        required=True
    )

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
        lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_CREATE)
        channel = await ctx.bot.rest.fetch_channel(ctx.options.channel)

        if ctx.options.language1 not in config['langs']:
            return await ctx.edit_response(f'There are no language named `{ctx.options.language1}`')
        if ctx.options.language2 not in config['langs']:
            return await ctx.edit_response(f'There are no language named `{ctx.options.language2}`')
        if isinstance(channel, hikari.GuildVoiceChannel):
            return await ctx.edit_response(f'You cannot set a voice channel as auto translate channel')
        if isinstance(channel, hikari.GuildCategory):
            return await ctx.edit_response(f'You cannot set a category as auto translate channel')
        
        data = {
            'guild_id': f'{ctx.get_guild().id}',
            'channel_id': f'{channel.id}',
            'lang1': f'{ctx.options.language1}',
            'lang2': f'{ctx.options.language2}'
        }

        if multiat.find_one({'channel_id': f'{channel.id}'}):
            return await ctx.edit_response(f'<#{channel.id}>, It is already an multi translate channel')
        else:
            multiat.insert_one(data)
        await ctx.edit_response(f'<#{channel.id}>, It is now the new auto translate channel')


def load(bot: Bot) -> None:
    bot.add_slash_command(MultiTrans)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('MultiTrans')
