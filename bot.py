import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

class Sally:
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
    
    @bot.command()
    async def add(ctx, left: int, right: int):
        await ctx.send(left + right)
    
    def main():
        bot.run(TOKEN)


if __name__ == '__main__':
    Sally.main()
