import os
import discord

TOKEN = os.environ.get('TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))

    async def on_message(self, message):
        channel = message.channel
        if self.user == message.author:
            return
        elif channel is not None:
            to_send = (f'Message from: {message.author}')
            await channel.send(to_send)


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    
    client = MyClient(intents=intents)
    client.run(TOKEN)
