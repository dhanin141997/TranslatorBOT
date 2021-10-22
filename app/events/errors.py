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


import hikari
import lightbulb
from lightbulb.events import SlashCommandErrorEvent
from lightbulb import errors
from app import Bot



class ErrorHandler(lightbulb.Plugin):
    
    @lightbulb.plugins.listener(SlashCommandErrorEvent)
    async def on_error(self, event: SlashCommandErrorEvent) -> None:
        if isinstance(event.exception, (errors.CommandNotFound, errors.OnlyInGuild)):
            return
        elif isinstance(event.exception, errors.MissingRequiredPermission):
            await event.context.respond(f'You are missing `{event.exception.permissions}` Permission(s)')
        elif isinstance(event.exception, errors.CommandInvocationError):
            if isinstance(event.exception.original, hikari.ForbiddenError):
                if event.exception.original.code == 50_007:
                    await event.context.respond('Your DM is closed')
                if event.exception.original.code == 50_001:
                    await event.context.edit_response('I have no access to this channel')


def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler)

def unload(bot: Bot) -> None:
    bot.remove_plugin('ErrorHandler')
