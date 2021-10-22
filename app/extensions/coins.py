import hikari
from hikari.interactions.base_interactions import ResponseType
import lightbulb
from lightbulb import slash_commands
from time import time
from random import randrange
from captcha.image import ImageCaptcha
from os import remove
import asyncio
from app import *



class Coins(slash_commands.SlashCommandGroup):
    description = 'Coins options'



@Coins.subcommand()
class Amount(slash_commands.SlashSubCommand):
    description = 'Use this command to show your coins amount'

    member: hikari.User = slash_commands.Option(
        'Pick a member to show his coins amount',
        required=False
    )

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check),
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        member = ctx.options.member or ctx.member.id
        member = await ctx.bot.rest.fetch_user(member)

        usr = usr_card.find_one({'user_id': f'{member.id}'})
        if not usr:
            data = {
                'user_id': f'{member.id}',
                'coins': 0,
                'rps': 0,
                'rps_time_after': f'{int(time())}',
                'time_after': f'{int(time())}'
            }
            usr_card.insert_one(data)
        usr = usr_card.find_one({'user_id': f'{member.id}'})

        await ctx.respond(f'**{member.username}**, Has `{int(usr["coins"]):,}`')



@Coins.subcommand()
class Daily(slash_commands.SlashSubCommand):
    description = 'Use this command to get your daily of coins'

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_CREATE)
        if usr := usr_card.find_one({'user_id': f'{ctx.member.id}'}):
            if usr['time_after'] <= str(int(time())):
                daily = randrange(200, 800)
                data = {
                    'user_id': f'{usr["user_id"]}',
                    'coins': usr['coins'] + daily,
                    'rps': usr['rps'],
                    'rps_time_after': usr['rps_time_after'],
                    'time_after': f'{int(time()) + 86400}'
                }
                usr_card.update_one({'user_id': f'{ctx.member.id}'}, {'$set': data})
                await ctx.edit_response(f'You got `{daily}` for today, come back (<t:{int(time()) + 86400}:R>, <t:{int(time()) + 86400}:t>)')
            else:
                await ctx.edit_response(f'Try again (<t:{usr["time_after"]}:R>, <t:{usr["time_after"]}:t>)')
        else:
            data = {
                'user_id': f'{ctx.member.id}',
                'coins': 0,
                'rps': 0,
                'rps_time_after': f'{int(time())}',
                'time_after': f'{int(time())}'
            }
            usr_card.insert_one(data)
            usr = usr_card.find_one({'user_id': f'{ctx.member.id}'})

            if usr['time_after'] <= str(int(time())):
                daily = randrange(200, 800)
                data = {
                    'user_id': f'{usr["user_id"]}',
                    'coins': usr['coins'] + daily,
                    'rps': usr['rps'],
                    'rps_time_after': usr['rps_time_after'],
                    'time_after': f'{int(time()) + 86400}'
                }
                usr_card.update_one({'user_id': f'{ctx.member.id}'}, {'$set': data})
                await ctx.edit_response(f'You\'ve got `{daily}` for today, come back (<t:{int(time()) + 86400}:R>, <t:{int(time()) + 86400}:t>)')
            else:
                await ctx.edit_response(f'Try again (<t:{usr["time_after"]}:R>, <t:{usr["time_after"]}:t>)')



@Coins.subcommand()
class Transfer(slash_commands.SlashSubCommand):
    description = 'Use this command to transfer coins to user'

    user: hikari.User = slash_commands.Option(
        'Pick a user to give him a coins',
        required=True
    )
    amount: int = slash_commands.Option(
        'Put the amount that you want to send',
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
            return ctx.edit_response('You cannot give respect point to a bot')
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
        for_usr = usr_card.find_one({'user_id': f'{ctx.options.user}'})
        if ctx.member.id == for_usr['user_id']:
            return await ctx.edit_response('You cannot transfer to yourself')
        if ctx.options.amount > usr['coins']:
            return await ctx.edit_response('You don\'t have that much of coins')
        
        num = str(randrange(1001, 9999))
        img = ImageCaptcha()
        img.write(num, f'{ctx.member.id}.png')

        amount_with_fees = int(ctx.options.amount * 0.03)
        amount_total = ctx.options.amount - amount_with_fees

        await ctx.edit_response(content=f'**{ctx.member.mention}, Transfer Fees: `{amount_with_fees:,}`, Amount: `{amount_total:,}`**\nType this numbers to confirm transfering', attachment=f'{ctx.member.id}.png')

        try:
            waited = await ctx.bot.wait_for(hikari.MessageCreateEvent, 20, lambda e: e.author.id == ctx.member.id)
        except asyncio.TimeoutError:
            return await ctx.delete_response()

        if waited.message.content == num:
            usr_data = {
                'user_id': f'{ctx.member.id}',
                'coins': usr['coins'] - ctx.options.amount,
                'rps': usr['rps'],
                'rps_time_after': usr['rps_time_after'],
                'time_after': usr['time_after']
            }
            for_usr_data = {
                'user_id': for_usr['user_id'],
                'coins': for_usr['coins'] + amount_total,
                'rps': for_usr['rps'],
                'rps_time_after': for_usr['rps_time_after'],
                'time_after': for_usr['time_after']
            }
            usr_card.update_one({'user_id': f'{ctx.member.id}'}, {'$set': usr_data})
            usr_card.update_one({'user_id': f'{ctx.options.user}'}, {'$set': for_usr_data})
            await ctx.delete_response()
            await ctx.followup(f'You transfered `{amount_total:,}`, to <@{for_usr["user_id"]}>')
            await waited.message.delete()
        else:
            await ctx.delete_response()
        remove(f'{ctx.member.id}.png')




def load(bot: Bot) -> None:
    bot.add_slash_command(Coins)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Coins')