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


from json import load
import lightbulb as lb
from pymongo import MongoClient


with open('config.json') as jsonfile:
    config = load(jsonfile)


client = MongoClient(config['client'])
db = client.get_database('database')
autotrans_channels   = db.autotrans_channels
multiat              = db.multiat
autotranslated_words = db.autotranslated_words
translated_words     = db.translated_words
usr_lvl              = db.usr_lvl
blacklist            = db.blacklist
dislvl               = db.dislvl
status               = db.status
usr_card             = db.usr_card


def black_check(ctx: lb.slash_commands.SlashCommandContext) -> bool:
    if usr := blacklist.find_one({'user_id': f'{ctx.member.id}'}):
        return False
    else:
        return True

def guild_black_check(ctx: lb.slash_commands.SlashCommandContext) -> bool:
    if guild := blacklist.find_one({'guild_id': f'{ctx.get_guild().id}'}):
        return False
    else:
        return True

def guild_owner(ctx: lb.slash_commands.SlashCommandContext) -> bool:
    return ctx.member.id == ctx.get_guild().owner_id
