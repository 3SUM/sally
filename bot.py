import re
import os
import json
import discord
from discord.ext import commands

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


class Sally:
    courses_list = ["135", "202", "218", "219", "370"]

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
                messages = await ctx.message.channel.history(limit=999).flatten()
                get_user_str = messages[-1].embeds[0].description.split("\n")
                user_id = int(re.sub("[^0-9]", "", get_user_str[0]))
                send_to = guild.get_member(user_id)
                with open("ticket.txt", "w") as file:
                    for message in reversed(messages):
                        file.write(
                            f"User: {message.author.name} -> {message.content}\n"
                        )
                with open("ticket.txt", "rb") as file:
                    dm_channel = await send_to.create_dm()
                    await dm_channel.send(
                        "Your ticket has been closed, attached is the ticket history:",
                        file=discord.File(file, "ticket.txt"),
                    )
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
        color = 0xCF65E7
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

        if "description" in data:
            desc = data["description"]

        if "color" in data:
            color = data["color"]

        ce = discord.Embed(
            title=title,
            description=desc,
            color=color,
        )

        if "fields" in data:
            for field in data["fields"]:
                ce.add_field(name=field["name"], value=field["value"], inline=False)

        if await ctx.send(embed=ce):
            await ctx.message.delete()

    @bot.command()
    async def ticket(ctx, course="default"):
        guild = ctx.message.guild
        request_channel = discord.utils.get(guild.channels, name="request")
        if ctx.message.channel != request_channel:
            failed_embed = discord.Embed(
                title="Failed to create a ticket",
                description=f"Ticket must be created in {request_channel.mention}!",
                color=0xE73C24,
            )
            await ctx.send(embed=failed_embed)
            return
        if str(course) in Sally.courses_list:
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
