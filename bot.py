import discord
from discord.ext import commands
import datetime
import os
import random
import traceback

# 봇 토큰
access_token = os.environ["BOT_TOKEN"]

client = discord.Client()


# client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print("Bot is ready.")
    print(client.user.name)
    print(client.user.id)
    print("--------------------")

    # 봇 상태
    await client.change_presence(status=discord.Status.idle)

    # 봇 활동 (type: 0=하는중, 1=트위치 생방송중, 2=듣는중)
    await client.change_presence(activity=discord.Activity(name='Testing by owo#4555', type=0))


@client.event
async def on_message(message):
    # 개인 메시지
    if isinstance(message.channel, discord.DMChannel):
        # 받은 DM을 포스팅할 채널
        channels = [672020127243304961, 672192045649231885]
        # 받음=빨강, 보냄=파랑
        embed = discord.Embed(description=message.author.mention + " -> " + client.user.mention,
                              colour=discord.Colour.red())
        if message.author == client.user:
            embed = discord.Embed(description=message.author.mention + " -> " + message.channel.recipient.mention,
                                  colour=discord.Colour.blue())

        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        from datetime import datetime
        now = datetime.now()
        now = now.strftime("%Y/%m/%d %I:%M:%S %p")
        embed.add_field(name=now, value=message.content, inline=True)
        embed.set_footer(text="ID: {0}".format(str(message.author.id), now))
        for x in channels:
            await client.get_channel(x).send(embed=embed)

    # 봇 명령어 (관리자만 가능)
    admins = [524980170554212363]
    if message.author.id in admins and message.author != client.user:

        if message.content.startswith("-test"):
            await message.channel.send("안녕하세요 {.mention}님.".format(message.author))

        if message.content.startswith("-getcode"):
            count = 1
            if len(message.content[8:]) > 0:
                count = int(message.content[8:10])
            for x in range(0, count):
                color = "%08x" % random.randint(0, 0xFFFFFFFF)
                daterand = random.randrange(29, 31)
                for x in range(1, 4):
                    color = color + "-" + "%08x" % random.randint(0, 0xFFFFFFFF)
                await message.channel.send(
                    color.upper() + "/ANY HyperFlick/Ultra +0.0833333333333333 days, 2020.1/" + str(daterand))

        if message.content.startswith("-dm"):
            author = message.mentions[0]
            msg = message.content[4:]
            msg = msg[msg.find(' ') + 1:]
            await author.send(msg)

        if message.content.startswith("-dmid"):
            author = message.guild.get_member(int(message.content[4:22]))
            msg = message.content[23:]
            await author.send(msg)

        if message.content.startswith("-embed"):
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title="Baby Shark",
                description="Dudududu"
            )

            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="ping", value="This has the bot say pong")
            embed.set_footer(text="This is a footer")
            await message.channel.send(embed=embed)

        if message.content.startswith('-say'):
            msg = message.content[5:]
            await message.channel.send(msg)

        if message.content.startswith('-tts'):
            msg = message.content[5:]
            await message.channel.send(msg, tts=True)

        if message.content.startswith('-diff'):
            msg = message.content[6:]
            await message.channel.send("```diff\n{0}\n```".format(msg))

    # 봇 명령어 (공통)
    if message.content.startswith("-cmds"):
        await message.channel.send(
            "```공용: -admins, -cmds, -info, -membercount, -배너볼래, -배너안볼래\n관리자: -dm, -dmid, -tts, -say, -diff, -embed, -getcode, -test\n```")

    if message.content.startswith("-info"):
        author = message.author
        if len(message.content[6:]) > 0:
            author = message.mentions[0]
        import datetime
        date = datetime.datetime.utcfromtimestamp(((int(author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(
            description=author.mention,
            colour=discord.Colour.green()
        )
        embed.add_field(name="이름", value=author, inline=True)
        embed.add_field(name="서버닉네임", value=author.display_name, inline=True)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일",
                        inline=True)
        embed.add_field(name="아이디", value=author.id, inline=True)
        embed.set_thumbnail(url=author.avatar_url)
        await message.channel.send("", embed=embed)

    if message.content.startswith("-membercount"):
        await message.channel.send(f"""$ of Members {message.guild.member_count}""")

    if message.content.startswith("-admins"):
        admins_str = ""
        for x in admins:
            admins_str += message.guild.get_member(x).mention + ", "
        await message.channel.send(admins_str)

    if message.content.startswith("-배너안볼래"):
        antibanner_role = message.guild.get_role(672364190937382970)
        if antibanner_role in message.author.roles:
            # await message.channel.send("`이미 가려졌습니다.`")
            return
        await message.author.add_roles(antibanner_role)
        embed = discord.Embed(
            description="배너가 완벽하게 가려졌습니다.",
            colour=discord.Colour.orange()
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text="다시 보려면 '-배너볼래'를 입력하세요.")
        await message.channel.send(embed=embed)

    if message.content.startswith("-배너볼래"):
        antibanner_role = message.guild.get_role(672364190937382970)
        if not antibanner_role in message.author.roles:
            # await message.channel.send("`이미 보입니다.`")
            return
        await message.author.remove_roles(antibanner_role)
        embed = discord.Embed(
            description="배너가 다시 보입니다.",
            colour=discord.Colour.green()
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text="배너를 가릴려면 '-배너안볼래'를 입력하세요.")
        await message.channel.send(embed=embed)


client.run(access_token)
