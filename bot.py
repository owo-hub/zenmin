import discord
import datetime
import os
import random
import traceback

client = discord.Client()


@client.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("--------------------")
    await client.change_presence(activity=discord.Activity(name='Testing by owo#4555', type=1))


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        channel = client.get_channel(672020127243304961)
        embed = discord.Embed(
            description = message.author.mention + " -> " + client.user.mention,
            colour = discord.Colour.red()
        )
        if message.author == client.user:
            embed = discord.Embed(
                description = message.author.mention + " -> " + message.channel.recipient.mention,
                colour = discord.Colour.blue()
            )

        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        from datetime import datetime
        now = datetime.now()
        now = now.strftime("%Y/%m/%d %I:%M:%S %p")
        embed.add_field(name=now, value=message.content, inline=True)
        embed.set_footer(text="ID: {0}".format(str(message.author.id), now))
        await channel.send(embed=embed)

    if message.content.startswith("hi"):
        await message.channel.send("안녕하세요 주인님.")

    if message.content.startswith("!getcode"):
        count = 1
        if len(message.content[8:]) > 0:
            count = int(message.content[8:10])
        for x in range(0, count):
            color = "%08x" % random.randint(0, 0xFFFFFFFF)
            daterand = random.randrange(29, 31)
            for x in range(1, 4):
                color = color + "-" + "%08x" % random.randint(0, 0xFFFFFFFF)
            await message.channel.send(color.upper() + "/ANY HyperFlick/Ultra +0.0833333333333333 days, 2020.1/" + str(daterand))

    if message.content.startswith("-DM"):
        author = message.guild.get_member(int(message.content[4:22]))
        msg = message.content[23:]
        await author.send(msg)

    if message.content.startswith("-info"):
        author = message.author
        if len(message.content[6:]) > 0:
            author = message.mentions[0]
        import datetime
        date = datetime.datetime.utcfromtimestamp(((int(author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(
            description=message.author.mention,
            colour=discord.Colour.red()
        )
        embed.add_field(name="이름", value=author, inline=True)
        embed.add_field(name="서버닉네임", value=author.display_name, inline=True)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=True)
        embed.add_field(name="아이디", value=author.id, inline=True)
        embed.set_thumbnail(url=author.avatar_url)
        await message.channel.send("", embed=embed)

    if message.content.startswith("-embed"):
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title = "Baby Shark",
            description = "Dudududu"
        )

        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="ping", value="This has the bot say pong")
        embed.set_footer(text="This is a footer")
        await message.channel.send(embed=embed)

    if message.content.startswith("~users"):
        await message.channel.send(f"""$ of Members {client.get_guild(671980240653778983).member_count}""")

    if message.content.startswith('!tts'):
        msg = message.content[5:]
        await message.channel.send(msg, tts=True)


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
