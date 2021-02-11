import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

class Sally:
    courses = [
        '135',
        '202',
        '218',
        '219',
        '370'
    ]

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
    
    @bot.command()
    async def add(ctx, left: int, right: int):
        await ctx.send(left + right)

    @bot.command()
    async def ticket(ctx, course):
        if str(course) in Sally.courses:
            await ctx.send(f'Selected course ticket: {course}')
        else:
            await ctx.send(f'`!ticket <course number>`\n\n access course number options using `!classes`')

    @bot.command()
    async def classes(ctx):
        await ctx.send(f'```\n135\n202\n218\n219\n370```')
    
    def main():
        bot.run(TOKEN)


if __name__ == '__main__':
    Sally.main()
