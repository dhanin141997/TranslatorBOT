import hikari
from hikari.interactions.base_interactions import ResponseType
import lightbulb
from lightbulb import slash_commands
from time import time
from app import *



class RP(slash_commands.SlashCommand):
    description = 'Use this command to give a respect point to a user'

    user: hikari.User = slash_commands.Option(
        'Pick a user to give him a respect point',
        required=True
    )

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_CREATE)
        usr = usr_card.find_one({'user_id': f'{ctx.member.id}'})
        for_usr = await ctx.bot.rest.fetch_user(ctx.options.user)
        if for_usr.is_bot:
            return await ctx.edit_response('You cannot give respect point to a bot')
        if ctx.member.id == for_usr.id:
            return await ctx.edit_response('You cannot give respect point to yourself')
        for_usr = usr_card.find_one({'user_id': f'{for_usr.id}'})

        if not usr:
            data = {
                'user_id': f'{ctx.member.id}',
                'coins': 0,
                'rps': 0,
                'rps_time_after': f'{int(time())}',
                'time_after': f'{int(time())}'
            }
            usr_card.insert_one(data)
        if not for_usr:
            data = {
                'user_id': f'{ctx.options.user}',
                'coins': 0,
                'rps': 0,
                'rps_time_after': f'{int(time())}',
                'time_after': f'{int(time())}'
            }
            usr_card.insert_one(data)
        
        usr = usr_card.find_one({'user_id': f'{ctx.member.id}'})
        for_usr = usr_card.find_one({'user_id': f'{ctx.options.user}'})

        if usr['rps_time_after'] <= str(int(time())):
            usr_data = {
                'user_id': usr['user_id'],
                'coins': usr['coins'],
                'rps': usr['rps'],
                'rps_time_after': f'{int(time()) + 43200}',
                'time_after': usr['time_after']
            }
            for_usr_data = {
                'user_id': for_usr['user_id'],
                'coins': for_usr['coins'],
                'rps': for_usr['rps']+1,
                'rps_time_after': for_usr['rps_time_after'],
                'time_after': for_usr['time_after']
            }
            usr_card.update_one({'user_id': f'{ctx.member.id}'}, {'$set': usr_data})
            usr_card.update_one({'user_id': f'{ctx.options.user}'}, {'$set': for_usr_data})
            await ctx.edit_response(f'You gave <@{for_usr["user_id"]}> a respect point')
        else:
            await ctx.edit_response(f'Try again (<t:{usr["rps_time_after"]}:R>, <t:{usr["rps_time_after"]}:t>)')


def load(bot: Bot) -> None:
    bot.add_slash_command(RP)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('RP')