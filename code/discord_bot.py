import discord
import asyncio

import dndbeyond_scraper

class DicecordBot:
    def __init__(self, token):
        self.token = token
        self.servers = {}
        try:
            self.readServers()
        except FileNotFoundError:
            pass
        self.scraper = dndbeyond_scraper.DnDBeyond()

    def startBot(self):
        self.loop = asyncio.new_event_loop()
        self.client = discord.Client(loop=self.loop)

        @self.client.event
        async def on_ready():
            """Print details and update server count when bot comes online."""
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')
            await self.client.change_presence(activity=discord.Game(name='PM "help" for commands'))

        @self.client.event
        async def on_message(message):
            await self.handle_message(message)

    async def handle_message(self, message):
        pass

    def readServers(self):
        pass
