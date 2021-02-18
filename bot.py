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
            guild = ctx.message.guild
            await guild.create_text_channel(f'ticket-{course}-{ctx.message.author}')
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
        
        content = message.content.upper()
        if(content.find("THANK YOU") > -1):
            for i in message.mentions:
                if i != message.author and i != bot.user:
                    await message.channel.send(f'Gave +1 Rep to {i.mention}')
        await bot.process_commands(message)

    def main():
        bot.run(TOKEN)


if __name__ == '__main__':
    Sally.main()
