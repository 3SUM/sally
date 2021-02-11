import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')

class Sally:
    def __init__(self, bot):
        self.bot = bot

    @bot.event
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')
    
    @bot.command()
    async def add(self, ctx, left: int, right: int):
        await ctx.send(left + right)
    
    def main(self):
        self.bot.run(TOKEN)


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    sally = Sally(bot)
    sally.main()
