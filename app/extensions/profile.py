import hikari
from hikari.embeds import Embed
from hikari.interactions.base_interactions import ResponseType
from hikari.files import Resourceish
import lightbulb
from easy_pil import Font, Editor, load_image_async
from math import ceil, floor
from lightbulb import slash_commands
from time import time
from app import *



class Profile(slash_commands.SlashCommand):
    description = 'Shows your profile or a user profile'

    user: hikari.User = slash_commands.Option('Pick a user or let it empty to show your profile', required=False)

    checks = [
        lightbulb.guild_only,
        lightbulb.Check(black_check),
        lightbulb.Check(guild_black_check)
    ]

    async def callback(self, ctx: slash_commands.SlashCommandContext) -> None:
        await ctx.interaction.create_initial_response(ResponseType.DEFERRED_MESSAGE_CREATE)
        user = ctx.options.user or ctx.member.id
        user = await ctx.bot.rest.fetch_user(user)
        bg = Editor('img/bg.png')
        usr = usr_lvl.find_one({'user_id': f'{user.id}'})
        if not usr:
            data = {
                'user_id': f'{user.id}',
                'exp': 0,
                'level': 0
            }
            usr_lvl.insert_one(data)
        card = usr_card.find_one({'user_id': f'{user.id}'})
        if not card:
            data = {
                'user_id': f'{user.id}',
                'coins': 0,
                'rps': 0,
                'time_after': f'{int(time())}'
            }
            usr_card.insert_one(data)
        
        avt = await load_image_async(str(user.avatar_url))
        avt = Editor(avt).resize((110, 110)).circle_image()
        circle = Editor('img/pop.png').resize((300, 300), crop=True).circle_image()

        poppins = Font().poppins(size=30)
        poppins_small = Font().poppins(size=20)
        poppins_small_s = Font().poppins(size=15)

        percent = usr['exp'] - (floor(usr['exp'] / 2000) * 2000)
        percent = int(percent / 2000 * 100)

        exp_left = ceil(usr['exp'] / 2000) * 2000

        exp_left = f'{exp_left:,}'
        exp_left = exp_left.split(',')
        exp = f'{usr["exp"]:,}'
        exp = exp.split(',')

        def checknum(num):
            if num[1][:2] == '00':
                num = f'{num[0]}'
            else:
                num = f'{num[0]}.{num[1][:2]}'
            return num
        

        if len(exp_left) == 2:
            exp_left = checknum(exp_left)
            exp_left = f'{exp_left}K'
        elif len(exp_left) == 3:
            exp_left = checknum(exp_left)
            exp_left = f'{exp_left}M'
        elif len(exp_left) == 4:
            exp_left = checknum(exp_left)
            exp_left = f'{exp_left}B'
        

        if len(exp) == 1:
            exp = exp[0]
        elif len(exp) == 2:
            exp = checknum(exp)
            exp = f'{exp}K'
        elif len(exp) == 3:
            exp = checknum(exp)
            exp = f'{exp}M'
        elif len(exp) == 4:
            exp = checknum(exp)
            exp = f'{exp}B'
        
        top = usr_lvl.find().sort('exp', -1)
        for num, rank in enumerate(top):
            if rank['user_id'] == usr['user_id']:
                num += 1
                break
        

        bg.paste(circle.image, (-110, -65))
        bg.paste(avt.image, (30, 25))

        bg.text((130, 20), f'+{card["rps"]}', poppins_small, 'white')
        bg.text((210, 10), f'{user.username}', poppins, 'white')
        bg.text((210, 80), f'LEVEL', poppins_small, 'white')
        bg.text((265, 70), f'{usr["level"]:,}', poppins, 'white')
        bg.text((340, 80), f'RANK', poppins_small, 'white')
        bg.text((395, 70), f'#{num:,}', poppins, 'white')
        bg.rectangle((205, 110), width=275, height=31, radius=20, fill='white')
        bg.bar((210, 113), max_width=270, height=25, radius=20, fill='#C39C9C', percentage=percent)
        bg.text((310, 115), f'{exp}/{exp_left}', poppins_small_s, 'black')


        await ctx.edit_response(attachment=bg.image_bytes)


def load(bot: Bot) -> None:
    bot.add_slash_command(Profile)

def unload(bot: Bot) -> None:
    bot.remove_slash_command('Profile')