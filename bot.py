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
    async def ticket(ctx, course = "default"):
        if str(course) in Sally.courses:
            await ctx.send(f'Selected course ticket: {course}')
        else:
            await ctx.send(f'`!ticket <course number>`\n\nAccess course number options using `!classes`')

    @bot.command()
    async def classes(ctx):
        await ctx.send(f'Course Number Options:  `135`  `202`  `218`  `219`  `370`')
    
    @bot.event
    async def on_message(message):
        if(message.author == bot.user):
            return
        
        await message.channel.send(f'Message sent by {message.author}')
        if(message.content.find("Thank you") > -1):
            await message.channel.send(f'Thank you {message.author}')

    def main():
        bot.run(TOKEN)


if __name__ == '__main__':
    Sally.main()
