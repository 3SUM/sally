import os
import json
import discord
from discord.ext import commands

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
#bot.remove_command('help')

class Sally:
    courses_list = ["135", "202", "218", "219", "370"]
    #cmd_list = ["close, courses, embed, help, ticket"]

    @bot.event
    async def on_guild_join(guild):
        if discord.utils.get(guild.categories, name="Server Stats") is None:
            category = await guild.create_category(name="Server Stats")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False)
            }
            await guild.create_voice_channel(
                name=(f"Member Count: {guild.member_count}"),
                overwrites=overwrites,
                category=category,
            )
        if discord.utils.get(guild.categories, name="Tickets") is None:
            category = await guild.create_category(name="Tickets")

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name="Student")
        await discord.Member.add_roles(member, role)

        channel = discord.utils.get(
            guild.voice_channels, name=(f"Member Count: {guild.member_count - 1}")
        )
        if channel:
            await channel.edit(name=(f"Member Count: {guild.member_count}"))

    @bot.event
    async def on_member_remove(member):
        guild = member.guild
        channel = discord.utils.get(
            guild.voice_channels, name=(f"Member Count: {guild.member_count + 1}")
        )
        if channel:
            await channel.edit(name=(f"Member Count: {guild.member_count}"))

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

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
            await ctx.send(
                "You do not have the necessary permissions to close a ticket!"
            )

    @bot.command()
    async def courses(ctx):
        await ctx.send(f"Course Number Options:  `135`  `202`  `218`  `219`  `370`")

    @bot.command()
    async def embed(ctx, *, message):
        color = None
        data = None
        desc = None
        title = None

        try:
            data = json.loads(message)
        except:
            await ctx.send("`embed`: Error, JSON format invalid!")
            return

        try:
            title = data["title"]
        except:
            await ctx.send("`embed`: Error, no title provided!")
            return

        try:
            desc = data["description"]
        except:
            desc = ""
        
        try:
            color = data["color"]
        except:
            color = 0xCF65E7

        ce = discord.Embed(
            title=title,
            description=desc,
            color=color,
        )

        try:
            for field in data["fields"]:
                ce.add_field(name=field["name"], value=field["value"], inline=False)
        except:
            print("No fields!")

        await ctx.send(embed=ce)
"""
    @bot.command()
    async def help(ctx, cmd="default"):
        if str(cmd) in Sally.cmd_list:
            pass
        else:
            help_menu = discord.Embed(
                title="Help Menu",
                description="Use !help <command> for more information\n"
                color=0xE9A7F7,
            )

            help_menu.add_field(name='**Tickets**', value=f'```fix\nticket```', inline=True)
            await ctx.send(embed=help_menu)
 """           

        

    @bot.command()
    async def ticket(ctx, course="default"):
        if str(course) in Sally.courses_list:
            guild = ctx.message.guild
            if discord.utils.get(
                guild.channels,
                name=(f"ticket-{course}-{ctx.message.author.name.lower()}"),
            ):
                failed_embed = discord.Embed(
                    title="Failed to create a ticket",
                    description="You already have a ticket open, please don't try to open a ticket while you already have one.",
                    color=0xE73C24,
                )
                await ctx.send(embed=failed_embed)
            else:
                category = discord.utils.get(guild.categories, name="Tickets")
                ta = discord.utils.get(guild.roles, name=course)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(
                        read_messages=False
                    ),
                    ctx.message.author: discord.PermissionOverwrite(read_messages=True),
                    ta: discord.PermissionOverwrite(read_messages=True),
                }
                ticket_create = await guild.create_text_channel(
                    name=(f"ticket-{course}-{ctx.message.author.name}"),
                    overwrites=overwrites,
                    category=category,
                )
                ticket_embed = discord.Embed(
                    title="Ticket",
                    description=(
                        f"{ctx.message.author.mention}\nPlease ask your question and a TA will be with you shortly."
                    ),
                    color=0x15A513,
                )
                ticket_embed.set_footer(
                    text=(f"Ticket requested by {ctx.message.author}"),
                    icon_url=ctx.message.author.avatar_url,
                )
                await ticket_create.send(embed=ticket_embed)
                success_embed = discord.Embed(
                    title="Ticket Creation",
                    description=(
                        f"{ctx.message.author.mention}, your ticket was successfully created: {ticket_create.mention}"
                    ),
                    color=0x15A513,
                )
                await ctx.send(embed=success_embed)
        else:
            await ctx.send(
                f"`!ticket <course number>`\n\nInvalid course number, refer to `!courses`"
            )

    def main():
        bot.run(TOKEN)


if __name__ == "__main__":
    Sally.main()
