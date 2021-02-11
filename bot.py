import os
import discord

TOKEN = os.environ.get('TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    
    client = MyClient(intents=intents)
    client.run(TOKEN)
