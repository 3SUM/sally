import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

class Sally:
    courses_list = [
        '135',
        '202',
        '218',
        '219',
        '370'
    ]

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        guild = discord.utils.get(bot.guilds, name="SALLY HQ")
        if guild is not None:
            if discord.utils.get(guild.categories, name="Server Stats") is None:
                category = await guild.create_category(name="Server Stats")
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(connect=False)
                }
                await guild.create_voice_channel(
                    name=(f'Member Count: {guild.member_count}'),
                    overwrites=overwrites,
                    category=category
                )
    
    @bot.command()
    async def close(ctx):
        guild = ctx.message.guild
        member = ctx.message.author
        member_roles = member.roles
        ta_role = discord.utils.get(guild.roles, name="TA")
        if ta_role in member_roles:
            if ctx.message.channel.name.find("ticket") > -1:
                await ctx.message.channel.delete()
            else:
                await ctx.send("Unable to close, this is not a ticket!")
        else:
            await ctx.send("You do not have the necessary permissions to close a ticket!")

    @bot.command()
    async def ticket(ctx, course = "default"):
        if str(course) in Sally.courses_list:
            guild = ctx.message.guild
            if discord.utils.get(guild.channels, name=(f'ticket-{course}-{ctx.message.author.name.lower()}')):
                failed_embed = discord.Embed(
                    title="Failed to create a ticket",
                    description="You already have a ticket open, please don't try to open a ticket while you already have one.",
                    color=0xe73c24
                )
                await ctx.send(embed=failed_embed)
            else:
                ta = discord.utils.get(guild.roles, name=course)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.message.author: discord.PermissionOverwrite(read_messages=True),
                    ta: discord.PermissionOverwrite(read_messages=True)
                }
                ticket_create = await guild.create_text_channel(
                    name=(f'ticket-{course}-{ctx.message.author.name}'),
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
            await ctx.send(f'`!ticket <course number>`\n\nInvalid course number, refer to `!courses`')

    @bot.command()
    async def courses(ctx):
        await ctx.send(f'Course Number Options:  `135`  `202`  `218`  `219`  `370`')
    
    @bot.event
    async def on_member_join(member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name="Student")
        await discord.Member.add_roles(member, role)

        print(discord.utils.get(guild.categories))
        if(discord.utils.get(guild.categories, name="Text Channels")):
            print("category exists")


    
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
