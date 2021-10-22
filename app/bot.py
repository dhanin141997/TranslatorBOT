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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import hikari
import lightbulb
from pytz import utc
import logging
from os import listdir
from app.app import *



class Bot(lightbulb.Bot):
    def __init__(self) -> None:
        self._extensions = [filename[:-3] for filename in listdir('./app/extensions') if filename.endswith('.py')]
        self._events = [filename[:-3] for filename in listdir('./app/events') if filename.endswith('.py')]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
    
        super().__init__(
            token=config['token'],
            slash_commands_only=True
        )
    
    
    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.stopping)

        super().run(
            activity=hikari.Activity(
                name=status.find_one({'id': 'status'})['status'],
                type=hikari.ActivityType.PLAYING
            )
        )
    
    async def starting(self, event: hikari.StartingEvent) -> None:
        for ext in self._extensions:
            self.load_extension(f'app.extensions.{ext}')
            logging.info(f'{ext} Loaded')
        for event in self._events:
            self.load_extension(f'app.events.{event}')
            logging.info(f'{event} Loaded')
    
    async def started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        logging.info('I am in')
    
    async def stopping(self, event: hikari.StoppingEvent) -> None:
        self.scheduler.shutdown()
