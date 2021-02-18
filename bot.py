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
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.message.author: discord.PermissionOverwrite(read_messages=True)
            }
            ticket_create = await guild.create_text_channel(
                name=(f'ticket-{course}-{ctx.message.author}'),
                overwrites=overwrites
            )
            ticket_embed = discord.Embed(
                title="Ticket",
                description=(f'{ctx.message.author.mention}\nPlease be patient. A TA will be with you shortly.'),
                color=0x15a513
            )
            ticket_embed.set_footer(
                text=(f'Ticket requested by {ctx.message.author}'),
                icon_url=ctx.message.author.avatar_url
            )
            await ticket_create.send(embed=ticket_embed)
            success_embed = discord.Embed(
                title="Ticket Creation",
                description=(f'{ctx.message.author.mention}, your ticket was successfully created: {ticket_create.mention}'),
                color=0x15a513
            )
            await ctx.send(embed=success_embed)
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
