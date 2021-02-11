import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

class Sally:
    courses = [
        135,
        202,
        218,
        219,
        370
    ]

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
    
    @bot.command()
    async def add(ctx, left: int, right: int):
        await ctx.send(left + right)

    @bot.command()
    async def ticket(ctx, course: int):
        if course in Sally.courses:
            await ctx.send(f'Selected course tick: {course}')
        else:
            await ctx.send(f'Invalid course: {course}')
    
    def main():
        bot.run(TOKEN)


if __name__ == '__main__':
    Sally.main()
