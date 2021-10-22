import hikari
from hikari.interactions.base_interactions import ResponseType
from hikari.messages import MessageFlag
import lightbulb
from lightbulb import slash_commands
from lightbulb.slash_commands.context import SlashCommandContext
from app import *



class Remove(slash_commands.SlashCommandGroup):
    description = 'Use this commands to remove the auto translate channels'



@Remove.subcommand()
class Autotrans(slash_commands.SlashSubCommand):
    description = 'Use this command to remove a channel from auto translate system (Administrator Only)'

    channel: hikari.TextableChannel = slash_commands.Option(
        'Choose the channel that you want to remove the auto translate from it',
        required=True
    )

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
        lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        channel = await ctx.bot.rest.fetch_channel(ctx.options.channel)
        if not autotrans_channels.find_one({'channel_id': f'{channel.id}'}):
            return await ctx.respond(f'<#{channel.id}>, It is not an auto translate channel', flags=MessageFlag.EPHEMERAL)
        
        await ctx.respond(f'<#{channel.id}>, It is no longer an auto translate channel', flags=MessageFlag.EPHEMERAL)

        autotrans_channels.delete_one({'channel_id': f'{channel.id}'})



@Remove.subcommand()
class Multitrans(slash_commands.SlashSubCommand):
    description = 'Use this command to remove a channel from multi translate system (Administrator Only)'

    channel: hikari.TextableChannel = slash_commands.Option(
        'Choose the channel that you want to remove the auto translate from it',
        required=True
    )

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
        lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        channel = await ctx.bot.rest.fetch_channel(ctx.options.channel)
        if not multiat.find_one({'channel_id': f'{channel.id}'}):
            return await ctx.respond(f'<#{channel.id}>, It is not an auto translate channel', flags=MessageFlag.EPHEMERAL)
        
        await ctx.respond(f'<#{channel.id}>, It is no longer an auto translate channel', flags=MessageFlag.EPHEMERAL)

        multiat.delete_one({'channel_id': f'{channel.id}'})



@Remove.subcommand()
class All(slash_commands.SlashSubCommand):
    description = 'Use this command to remove all the channels from auto translate and multi translate system'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
        lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
    ]

    async def callback(self, ctx: SlashCommandContext) -> None:
        await ctx.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_CREATE)
        message = 'There no `autotrans`, `multitrans` channels in this server'
        if autotrans_channels.find_one({'guild_id': f'{ctx.get_guild().id}'}):
            autotrans_channels.delete_many({'guild_id': f'{ctx.get_guild().id}'})
            message = f'{ctx.member.mention}, Done'
        if multiat.find_one({'guild_id': f'{ctx.get_guild().id}'}):
            multiat.delete_many({'guild_id': f'{ctx.get_guild().id}'})
            message = f'{ctx.member.mention}, Done'
        
        await ctx.edit_response(message)


def load(bot: Bot) -> None:
    bot.add_slash_command(Remove)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Remove')