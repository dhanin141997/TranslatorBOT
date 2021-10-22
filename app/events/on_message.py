'''
   Copyright 2021 mear

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''


from __future__ import annotations
import hikari
from hikari.embeds import Embed
import lightbulb
from deep_translator import GoogleTranslator , single_detection
from re import search, Match
from random import randrange
from math import ceil
from time import time
from app import *




class OnMessage(lightbulb.Plugin):

    @lightbulb.plugins.listener(hikari.MessageCreateEvent)
    async def on_message(self, event: hikari.MessageCreateEvent) -> None:
        if event.message.author.is_bot or isinstance(await event.message.fetch_channel(), hikari.DMChannel):
            return
        if blacklist.find_one({'guild_id': f'{event.message.guild_id}'}) or blacklist.find_one({'user_id': f'{event.message.member.id}'}):
            return
        
        try:
            if (channel := autotrans_channels.find_one({'channel_id': f'{event.channel_id}'})):
                translate = GoogleTranslator(source='auto', target=channel['lang']).translate(text=event.message.content)
                emoji: Match = search(r'<a?:(\w+):(\d+)>', event.message.content)
                # emoji_slice = slice(emoji.start(), emoji.end())
                # print(event.message.content[emoji_slice])
                if translate.startswith('<@!') and translate.endswith('>'):
                    return
                else:
                    if emoji is None:
                        if event.message.content == translate:
                            return
                        elif translate is None:
                            return
                        else:
                            content = event.message.content
                            if content.startswith('<@!'):
                                length = len(translate)
                                trans_slice = slice(23, length)
                                msg_slice = slice(23)
                                msg_slice = content[msg_slice]
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                            else:
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                    'guild_id': f'{event.message.guild_id}',
                                    'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                    else:
                        if event.message.content == translate:
                            return
                        elif event.message.content == emoji['match']:
                            return
                        else:
                            content = event.message.content
                            if content.startswith('<@!'):
                                length = len(translate)
                                trans_slice = slice(23, length)
                                msg_slice = slice(23)
                                msg_slice = content[msg_slice]
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                    'guild_id': f'{event.message.guild_id}',
                                    'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                            else:
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                    'guild_id': f'{event.message.guild_id}',
                                    'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
        except: ...
        
        try:
            if dislvl.find_one({'guild_id': f'{event.message.guild_id}'}):
                return
            usr = usr_lvl.find_one({'user_id': f'{event.message.member.id}'})
            if usr:
                new_exp = usr['exp'] + randrange(1, 10)
                new_lvl = 1 if new_exp / 2000 < 1 else ceil(new_exp / 2000)
                data = {
                    'user_id': f'{event.message.member.id}',
                    'exp': new_exp,
                    'level': new_lvl
                }
                usr_lvl.update_one({'user_id': f'{event.message.member.id}'}, {'$set': data})
            else:
                data = {
                    'user_id': f'{event.message.member.id}',
                    'exp': randrange(1, 10),
                    'level': 0
                }
                usr_lvl.insert_one(data)
        except:...

        try:
            if channel := multiat.find_one({'channel_id': f'{event.message.channel_id}'}):
                if (GoogleTranslator(source=channel['lang1'], target=channel['lang2']).translate(event.message.content) != event.message.content) or (GoogleTranslator(source=channel['lang2'], target=channel['lang1']).translate(event.message.content) != event.message.content):
                    try:
                        dl = single_detection(event.message.content, api_key=config['dkey1'])
                    except:
                        try:
                            dl = single_detection(event.message.content, api_key=config['dkey2'])
                        except:
                            dl = single_detection(event.message.content, api_key=config['dkey3'])
                    if dl != channel['lang1'] and dl != channel['lang2']: return
                    if dl == channel['lang1']:
                        froml = channel['lang1']
                        tol = channel['lang2']
                    elif dl == channel['lang2']:
                        froml = channel['lang2']
                        tol = channel['lang1']
                # if GoogleTranslator(source=channel['lang1'], target=channel['lang2']).translate(event.message.content) == event.message.content:
                #     froml = channel['lang2']
                #     tol = channel['lang1']
                # else:
                #     froml = channel['lang1']
                #     tol = channel['lang2']
                translate = GoogleTranslator(source=froml, target=tol).translate(text=event.message.content)
                emoji: Match = search(r'<a?:(\w+):(\d+)>', event.message.content)
                # emoji_slice = slice(emoji.start(), emoji.end())
                # print(event.message.content[emoji_slice])
                if translate.startswith('<@!') and translate.endswith('>'):
                    return
                else:
                    if emoji is None:
                        if event.message.content == translate:
                            return
                        elif translate is None:
                            return
                        else:
                            content = event.message.content
                            if content.startswith('<@!'):
                                length = len(translate)
                                trans_slice = slice(23, length)
                                msg_slice = slice(23)
                                msg_slice = content[msg_slice]
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                            else:
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                    'guild_id': f'{event.message.guild_id}',
                                    'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                    else:
                        if event.message.content == translate:
                            return
                        elif event.message.content == emoji['match']:
                            return
                        else:
                            content = event.message.content
                            if content.startswith('<@!'):
                                length = len(translate)
                                trans_slice = slice(23, length)
                                msg_slice = slice(23)
                                msg_slice = content[msg_slice]
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                    'guild_id': f'{event.message.guild_id}',
                                    'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=msg_slice + ' ' + translate[trans_slice])
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                            else:
                                words = content.split()
                                get_translatewords = autotranslated_words.find_one({'guild_id': f'{event.message.guild_id}'})
                                if get_translatewords:
                                    new_count = get_translatewords['translated_words'] + len(words)
                                    updated_data = {
                                        'guild_id': f'{event.message.guild_id}',
                                        'translated_words': new_count
                                    }
                                    autotranslated_words.update_one({'guild_id': f'{event.message.guild_id}'}, {'$set': updated_data})
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
                                else:
                                    default_data = {
                                    'guild_id': f'{event.message.guild_id}',
                                    'translated_words': len(words)
                                    }
                                    autotranslated_words.insert_one(default_data)
                                    embed = Embed(color=0x2C3434, description=translate)
                                    embed.set_author(name=event.message.member.display_name, icon=event.message.member.avatar_url)
                                    await event.message.respond(embed=embed)
        except: ...

        try:
            if usr := usr_card.find_one({'user_id': f'{event.message.member.id}'}):
                new_coins = usr['coins'] + randrange(1, 10)
                data = {
                    'user_id': f'{event.message.member.id}',
                    'coins': new_coins,
                    'rps': usr['rps'],
                    'rps_time_after': usr['rps_time_after'],
                    'time_after': f'{usr["time_after"]}'
                }
                usr_card.update_one({'user_id': f'{event.message.member.id}'}, {'$set': data})
            else:
                data = {
                    'user_id': f'{event.message.member.id}',
                    'coins': randrange(1, 10),
                    'rps': 0,
                    'rps_time_after': f'{int(time())}',
                    'time_after': f'{int(time())}'
                }
                usr_card.insert_one(data)
        except: ...


def load(bot: Bot) -> None:
    bot.add_plugin(OnMessage)

def unload(bot: Bot) -> None:
    bot.remove_plugin(OnMessage)
