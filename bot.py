import discord
from discord.ext import commands
import urllib.parse, urllib.request, re
import datetime
import os
import random
import traceback
import bs4
import asyncio
import threading
import requests

access_token = os.environ["BOT_TOKEN"]

client = discord.Client()

log_channel = 683877528494014464
notice_channel = 656865311622168619
badword_list = ['^^ㅣ발', '^ㅣ발', '야발', '섹스', '느금마', '애미', '애비', '장애인', '느금', '보지', '자지', '니애미', 'badwordtest1', 'badwordtest2']
badwords = []
colours = [discord.Color.dark_orange(),discord.Color.orange(),discord.Color.dark_gold(),discord.Color.gold(),discord.Color.dark_magenta(),
           discord.Color.magenta(),discord.Color.red(),discord.Color.dark_red(),discord.Color.blue(),discord.Color.dark_blue(),discord.Color.teal(),
           discord.Color.dark_teal(),discord.Color.green(),discord.Color.dark_green(),discord.Color.purple(),discord.Color.dark_purple()]
regionals = {'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}', 'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
             'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
             'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}', 'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
             'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
             'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}', 'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
             'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
             'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}', 'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
             'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
             'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}', 'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
             'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
             'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}', 'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
             'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
             's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}', 't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
             'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
             'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}', 'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
             'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
             'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}', 'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
             '0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣',
             '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣', '8': '8⃣', '9': '9⃣', '!': '\u2757',
             '?': '\u2753', ' ': ' '}

# client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    from datetime import datetime
    print("Bot is ready.")
    print(client.user.name)
    print(client.user.id)
    print("--------------------")
    await client.change_presence(activity=discord.Streaming(platform='Twitch', name='젠민아 도와줘', url='https://www.twitch.tv/zenmin_ow/'))
    """embed=discord.Embed(
        description="**젠민봇**이 실행되었습니다.",
        timestamp=datetime.utcnow(),
        colour=discord.Color.gold()
    )
    embed.set_author(name=client.user, icon_url=client.user.avatar_url)
    await client.get_channel(log_channel).send(embed=embed)
    check = await client.get_channel(684157506972549159).send(embed=discord.Embed(description=f"🚨 젠민님을 좋아해서 이서버에 오셨습니까? 🚨\n{client.get_channel(notice_channel).mention} 꼭 확인하시고 선택해 주세요.", timestamp=datetime.utcnow(), colour=discord.Color.teal()))
    await check.add_reaction(emoji='✅')
    await check.add_reaction(emoji='❌')"""

"""@client.event
async def on_disconnect():
    from datetime import datetime
    embed = discord.Embed(
        description="**젠민봇**이 종료되었습니다.",
        timestamp=datetime.utcnow(),
        colour=discord.Color.red()
    )
    embed.set_author(name=client.user, icon_url=client.user.avatar_url)
    await client.get_channel(log_channel).send(embed=embed)"""

"""@client.event
async def on_reaction_add(reaction, user):
    global check
    zenmin_serverid = client.get_guild(656862634754310174)
    if reaction.message.channel == client.get_channel(684157506972549159):
        check_role = zenmin_serverid.get_role(684154195108036760)
        cross_role = zenmin_serverid.get_role(684159790762426377)
        if check_role in user.roles or cross_role in user.roles:
            return
        if reaction.emoji == "✅":
            await user.add_roles(check_role)
        elif reaction.emoji == "❌":
            await user.add_roles(cross_role)"""



@client.event
async def on_message(message):
    admins = [524980170554212363, 304164780288245761, 262812931924688897, 418167691904286720, 287124567003234304]
    welcome_channel = client.get_channel(656862634754310178)
    notice_channel = client.get_channel(656865311622168619)
    zenmin_serverid = client.get_guild(656862634754310174)

    if any(x in message.content for x in badword_list) and message.guild == zenmin_serverid:
        info = await message.channel.send(embed=discord.Embed(
            description=f"🚨 {message.author.mention} 님의 욕설이 감지됐습니다. 🚨",
            colour=discord.Color.dark_red()
        ))
        for badword in badword_list:
            if badword in message.content and not badword in badwords:
                badwords.append(badword)
        print(badwords)
        from datetime import datetime
        embed = discord.Embed(
            description=f"🚨 {message.author.mention} 님이 {message.channel.mention} 채널에서 **욕설**을 사용했습니다.",
            timestamp=datetime.utcnow(),
            colour=discord.Color.dark_red()
        )
        embed.set_author(name=message.author,
                         icon_url=message.author.avatar_url)
        embed.add_field(name="제거된 메시지", value=message.content)
        embed.add_field(name="감지된 욕설 ({0})".format(len(badwords)), value=", ".join(str(i) for i in badwords), inline=False)
        embed.set_footer(text="유저 ID: {0}".format(message.author.id))
        await message.delete()
        await client.get_channel(log_channel).send(embed=embed)
        # await asyncio.sleep(1)
        # await info.delete()

    # 개인 메시지
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        # 받은 DM을 포스팅할 채널
        dm_channels = [683877528494014464]
        # 받음=빨강, 보냄=파랑
        from datetime import datetime
        embed = discord.Embed(
                description=message.author.mention + " to " + client.user.mention,
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red()
        )
        """
        if message.author == client.user:
            embed = discord.Embed(
                    description=message.author.mention + " to " + message.channel.recipient.mention,
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.blue()
            )
        """
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name="받은 메시지:", value=message.content)
        embed.set_footer(text="ID: {0}".format(str(message.author.id)))
        for x in dm_channels:
            await client.get_channel(x).send(embed=embed)

    # 관리자 명령어
    if message.author.id in admins and message.author != client.user:

        if message.content.startswith(">>") and message.author != client.user:
            result = ''
            for x in range(2, len(message.content)):
                letter = message.content[x:x + 1].lower()
                if letter in regionals:
                    result = result + regionals[letter] + " "
                    print(result)
            if result != '':
                await message.channel.send(result)

        if message.content.startswith('젠민아 말해 '):
            msg = message.content[7:]
            await message.delete()
            await message.channel.send(msg)

        if message.content.startswith('젠민아 읽어 '):
            msg = message.content[7:]
            await message.delete()
            await message.channel.send(msg, tts=True)

        if message.content.startswith('-diff'):
            msg = message.content[6:]
            await message.channel.send("```diff\n{0}\n```".format(msg))

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

    # 자유 명령어
    if message.content.startswith("젠민아 도와줘"):
        from datetime import datetime
        embed = discord.Embed(
            title='저를 부를 땐 앞에 "젠민아"를 붙여주세요!',
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green()
        )
        embed.set_author(name='젠민봇 명령어 목록', icon_url=client.user.avatar_url)
        # embed.set_thumbnail(url=message.guild.icon_url)
        embed.add_field(name="관리자 명령어", value="`말해 {할말}`, `읽어 {할말}`", inline=False)
        embed.add_field(name="유저 명령어", value="`도와줘`, `안녕`, `멤버수`, `관리자`, `영웅추천 {포지션}`, `고마워`, `트위치`", inline=False)
        embed.add_field(name="검색 명령어", value="`누구야`, `유튜브`, `배틀태그`", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("젠민아 안녕"):
        await message.channel.send("안녕하세요, {.mention} 님!".format(message.author))

    if message.content.startswith("젠민아 누구야 "):
        author = message.author
        if len(message.content[8:]) > 0:
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

    if message.content.startswith("젠민아 고마워"):
        thankmsg = ["헤헿", "^^", " (っ˘ڡ˘ς) ", "{0} 저도 고마워요!".format(message.author.mention), "응"]
        await message.channel.send(random.choice(thankmsg))

    if message.content.startswith("젠민아 멤버수"):
        await message.channel.send(f"현재 **{message.guild.name}** 서버에는 **{message.guild.member_count}**명이 있습니다!")

    if message.content.startswith("젠민아 관리자"):
        embed = discord.Embed(
            description=f"**젠민봇**에 등록된 관리자는 총 **{len(admins)}**명이 있어요!\n"
                        f"{', '.join(message.guild.get_member(i).mention for i in admins)}\n\n"
                        f"⚠ 친한 사람 아니면 **DM** 자제해 주세요! ⚠",
            colour=discord.Color.dark_teal()
        )
        embed.set_footer(text="Powered by owo#4555")
        await message.channel.send(embed=embed)

    if message.content.startswith("젠민아 영웅추천"):
        tank = ["D.va", "라인하르트", "레킹볼", "로드호그", "시그마", "오리사", "윈스턴", "자리야"]
        damage = ["겐지", "둠피스트", "리퍼", "맥크리", "메이", "바스티온", "솔저: 76", "솜브라", "시메트라", "애쉬", "위도우메이커", "정크랫", "토르비욘", "트레이서", "파라", "한조"]
        support = ["루시우", "메르시", "모이라", "바티스트", "브리기테", "아나", "젠야타"]
        all_heroes = ["D.va", "겐지", "둠피스트", "라인하르트", "레킹볼", "로드호그",
                  "루시우", "리퍼", "맥크리", "메르시", "메이", "모이라", "바스티온", "바티스트", "브리기테",
                  "솔저: 76", "솜브라", "시그마", "시메트라", "아나", "애쉬", "오리사", "위도우메이커", "윈스턴",
                  "자리야", "정크랫", "젠야타", "토르비욘", "트레이서", "파라", "한조"]
        role = message.content[9:10].lower()

        if role == "탱":
            result = random.choice(tank)
        elif role == "딜":
            result = random.choice(damage)
        elif role == "힐":
            result = random.choice(support)
        else:
            result = random.choice(all_heroes)

        htm_content = urllib.request.urlopen("https://playoverwatch.com/ko-kr/heroes").read()
        htm_content = str(htm_content)
        print(htm_content)
        profile_img = re.findall(r'<img class="portrait" src="(https://.*?png)"', htm_content)

        print(profile_img)
        for i in profile_img:
            print(i)

        embed = discord.Embed(
            title=result,
            description=message.author.mention
        )

        for x in range(0, len(all_heroes)):
            print(result + ", " + all_heroes[x])
            if result == all_heroes[x]:
                embed.set_thumbnail(url=profile_img[x])
                break
        # await message.channel.send("{0.mention} **{1}** 하세요".format(message.author, result))
        await message.channel.send(embed=embed)

    if message.content.startswith("젠민아 유튜브 "):
        search = message.content[8:]
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        randomNum = random.randrange(0, len(search_results))
        print("총 {0}개 검색, {1}번 출력".format(len(search_results), randomNum))
        await message.channel.send(f'제가 찾은 "{search}"의 최신 동영상입니다.\nhttp://www.youtube.com/watch?v={search_results[0]}')

    if message.content.startswith("젠민아 배틀태그 "):
        tag = message.content[9:]
        battletag = tag.replace("#", "-")
        print(f"Replace tag '{tag}' to '{battletag}'")
        url = 'https://playoverwatch.com/ko-kr/career/pc/' + battletag
        url = urllib.parse.urlsplit(url)
        url = list(url)
        url[2] = urllib.parse.quote(url[2])
        profile_url = urllib.parse.urlunsplit(url)
        print(f"{tag}'s Profile: {profile_url}")
        htm_content = urllib.request.urlopen(profile_url).read()
        htm_content = bs4.BeautifulSoup(htm_content, 'html.parser')
        htm_content = str(htm_content)
        # print(f"Found HTML: {htm_content}")

        profile_img = re.findall(r'<img class="player-portrait" src="(https://.*?png)"', htm_content)
        if len(profile_img) < 1:
            print(f"Failed to find {tag}'s profile.")
            await message.channel.send("유저 정보를 찾을 수 없습니다.\n(배틀태그 검색은 대소문자를 구분하므로 대소문자를 정확히 입력해야 합니다.)")
            return

        isPublic = htm_content.find('<div class="masthead-permission-level-container u-center-block">') == -1
        print(f"Is profile public: {isPublic}")

        print("Profile icon: " + profile_img[0])
        quickplay_img = re.findall(r'data-js="heroMastheadImage" style="background-image: (https://.*?png)">', htm_content)
        player_level_img = htm_content[htm_content.find('<div class="player-level" style'):htm_content.find('<div class="player-rank" style')]
        player_level_img = re.findall(r' (https://.*?png) ', player_level_img)
        print(player_level_img)

        exist_tank = htm_content.find("돌격 실력 평점") != -1
        exist_damage = htm_content.find("공격 실력 평점") != -1
        exist_support = htm_content.find("지원 실력 평점") != -1
        print(f"돌격: {exist_tank}, 공격: {exist_damage}, 지원: {exist_support}")

        print(quickplay_img)

        from datetime import datetime
        embed = discord.Embed(
            title=f"🔗 프로필 링크",
            timestamp=datetime.utcnow(),
            # description=f"🔓 공개 프로필" if isPublic == True else f"🔒 비공개 프로필",
            colour=discord.Colour.orange(),
            url=profile_url
        )
        embed.set_author(name=tag, icon_url=profile_img[0])

        embed.set_footer(text=f"🔓 공개 프로필" if isPublic == True else f"🔒 비공개 프로필")
        if quickplay_img:
            embed.set_image(url=quickplay_img[0])

        if exist_tank or exist_damage or exist_support:
            if exist_tank:
                tank_html = htm_content[htm_content.find("돌격 실력 평점"):htm_content.find("돌격 실력 평점") + 200]
                tank_tier = re.findall(r'<img class="competitive-rank-tier-icon" src="(https://.*?png)"', tank_html)
                tank_level = re.findall(r'<div class="competitive-rank-level">(.*?)</div>', tank_html)
                embed.set_thumbnail(url=tank_tier[0])
                embed.add_field(name="돌격 실력 평점", value=f"```fix\n{tank_level[0]}```")
            if exist_damage:
                damage_html = htm_content[htm_content.find("공격 실력 평점"):htm_content.find("공격 실력 평점") + 200]
                damage_tier = re.findall(r'<img class="competitive-rank-tier-icon" src="(https://.*?png)"', damage_html)
                damage_level = re.findall(r'<div class="competitive-rank-level">(.*?)</div>', damage_html)
                embed.set_thumbnail(url=damage_tier[0])
                embed.add_field(name="공격 실력 평점", value=f"```fix\n{damage_level[0]}```")
            if exist_support:
                support_html = htm_content[htm_content.find("지원 실력 평점"):htm_content.find("지원 실력 평점") + 200]
                support_tier = re.findall(r'<img class="competitive-rank-tier-icon" src="(https://.*?png)"', support_html)
                support_level = re.findall(r'<div class="competitive-rank-level">(.*?)</div>', support_html)
                embed.set_thumbnail(url=support_tier[0])
                embed.add_field(name="지원 실력 평점", value=f"```fix\n{support_level[0]}```")
        else:
            embed.set_thumbnail(url=profile_img[0])
        await message.channel.send(embed=embed)

    if message.content.startswith("젠민아 서버정보"):
        findbots = sum(1 for message.author in message.guild.members if message.author.bot)

        embed = discord.Embed()

        if message.guild.icon:
            embed.set_thumbnail(url=message.guild.icon_url)
        if message.guild.banner:
            embed.set_image(url=message.guild.banner_url_as(format="png"))

        embed.add_field(name="Server Name", value=message.guild.name, inline=True)
        embed.add_field(name="Server ID", value=message.guild.id, inline=True)
        embed.add_field(name="Members", value=message.guild.member_count, inline=True)
        embed.add_field(name="Bots", value=findbots, inline=True)
        embed.add_field(name="Owner", value=message.guild.owner, inline=True)
        embed.add_field(name="Region", value=message.guild.region, inline=True)
        embed.add_field(name="Created", value=message.guild.created_at, inline=True)

        await message.channel.send(content=f"ℹ information about **{message.guild.name}**", embed=embed)

    if message.content.startswith("젠민아 입장테스트"):
        from datetime import datetime
        embed = discord.Embed(
            title="🔗 서버 재참가 링크",
            description=f"Hey! {message.author.mention},",
            timestamp = datetime.utcnow(),
            colour=random.choice(colours),
            url="https://discordapp.com/invite/E2PsZwH"
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text=f"유저 ID: {message.author.id}")
        # embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(
            name=f"Welcome to the **Overwatch Workshop** Community **OWOHUB** Server !",
            value=f"**오버워치 워크샵** 커뮤니티 **오떱헙** 서버에 오신것을 진심으로 환영합니다! 🎊"
        )
        embed.add_field(
            name=f"Don't forget to read the **annoucement**!",
            value=f"가끔 올라오는 공지사항 {notice_channel.mention}, 꼭 잊지 말고 읽어주세요!",
            inline=False
        )
        await message.author.send(embed=embed)
        await message.channel.send(message.author.mention, embed=embed)

    if message.content.startswith("젠민아 배너안볼래"):
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

    if message.content.startswith("젠민아 배너볼래"):
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

    if message.content.startswith("젠민아 유저정보 "):
        waiting = await message.channel.send(embed=discord.Embed(description='유저 정보를 불러오는중', color=discord.Color.blue()))
        if len(message.mentions) > 0:
            author = message.mentions[0]
        else:
            author = message.author
        import datetime
        registered = datetime.datetime.utcfromtimestamp(((int(author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(
            description=author.mention,
            colour=discord.Colour.red()
        )
        embed.set_author(name=author, icon_url=author.avatar_url)
        embed.add_field(name="Registered", value=f'{str(registered.year)}년 {str(registered.month)}월 {str(registered.day)}일')
        embed.add_field(name=f'Roles [{len(author.roles)-1}]',
                        value="".join(i.mention for i in author.roles if str(i) != '@everyone'),
                        inline=False)
        embed.set_footer(text=f"ID: {author.id}")
        await waiting.delete()
        await message.channel.send(embed=embed)

    if message.content == "젠민아 현재시간":
        import datetime
        utcnow = datetime.datetime.utcnow()
        time_gap = datetime.timedelta(hours=9)
        kor_time = utcnow + time_gap
        date = kor_time.strftime(f"%Y년 %m월 %d일 {'오전' if kor_time.strftime('%p') == 'AM' else '오후'} %I시 %M분")
        await message.channel.send(date)

    if message.content == "젠민아 트위치":
        ready = await message.channel.send(embed=discord.Embed(
            description="**젠민_**님의 트위치 정보를 읽어오고 있습니다.",
            colour=discord.Color.orange()
        ))

        embed = discord.Embed(
            description=f"[팔로워](https://www.twitch.tv/zenmin_ow/followers) **8,4781**명\n\n"
                        f"[🔗 언팔 하러 가기](https://www.twitch.tv/zenmin_ow/)\n"
                        f"[🔗 동영상 보러가기](https://www.twitch.tv/zenmin_ow/videos)\n"
                        f"[🔗 클립 보러가기](https://www.twitch.tv/zenmin_ow/clips)\n",
            colour=discord.Color.purple()
        )
        embed.set_author(name="젠민_ (zenmin_ow)",
                         icon_url="https://cdn3.iconfinder.com/data/icons/popular-services-brands-vol-2/512/twitch-512.png",
                         url="https://www.twitch.tv/zenmin_ow/")
        embed.set_footer(text="Powered by owo#4555")
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_image(url="https://static-cdn.jtvnw.net/jtv_user_pictures/5016f0de-3f43-4a01-9c9c-93f7eae02927-profile_banner-480.png")
        await asyncio.sleep(1)
        await ready.delete()
        await message.channel.send(embed=embed)

    if message.content.startswith("젠민아 손"):
        await message.channel.send("멍멍! (챱)")

    if message.content.startswith("젠민아 짖어"):
        await message.channel.send("푸르르.. 아잇! 어! 👏 🍜")

    if message.content.startswith("젠민아 기다려") or message.content.startswith("젠민아 앉아"):
        await message.channel.send("(쭈글)")

    if message.content.startswith("젠민아 산책"):
        await message.channel.send("위험해요... 😷")

    if message.content == "젠민아" or message.content == "젠민아 ":
        await message.channel.send("🦝?")

    if message.content.startswith('젠민아 청소 '):
        if message.author.guild_permissions.administrator:
            llimit = message.content[7:].strip()
            await message.channel.purge(limit=int(llimit)+1)
            from datetime import datetime
            embed = discord.Embed(
                description=f"🗑️ {message.author.mention} 님의 의해 **{int(llimit)}** 메시지가 삭제됐습니다.",
                # timestamp=datetime.utcnow(),
                colour=discord.Color.green()
            )
            await client.get_channel(log_channel).send(f"{message.channel.mention} 채널에서 청소", embed=embed)
            trash = await message.channel.send(embed=embed)
            await asyncio.sleep(2)
            await trash.delete()

@client.event
async def on_message_delete(message):
    if message.author.bot == False:
        from datetime import datetime
        embed = discord.Embed(
            description=f'🗑️ {message.author.mention} 님의 메시지가 삭제되었습니다.',
            timestamp=datetime.utcnow(),
            colour=discord.Color.red()
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name="채널", value=message.channel.mention, inline=False)
        embed.add_field(name="삭제된 메시지", value=message.content)
        embed.set_footer(text=f'유저 ID: {message.author.id}')
        await client.get_channel(log_channel).send(embed=embed)

@client.event
async def on_message_edit(before, after):
    from datetime import datetime
    if after.author.bot == False:
        embed = discord.Embed(
            description=f'🔄 {after.author.mention} 님의 메시지가 수정되었습니다. [메시지로 이동](https://discordapp.com/channels/{after.guild.id}/{after.channel.id}/{after.id})',
            timestamp=datetime.utcnow(),
            colour=discord.Color.blue()
        )
        embed.set_author(name=after.author, icon_url=after.author.avatar_url)
        embed.add_field(name="채널", value=after.channel.mention, inline=False)
        embed.add_field(name="수정 전", value=before.content, inline=False)
        embed.add_field(name="수정 후", value=after.content, inline=False)
        embed.set_footer(text=f'유저 ID: {after.author.id}')
        await client.get_channel(log_channel).send(embed=embed)

@client.event
async def on_member_update(before, after):
    from datetime import datetime
    if after.bot == False and before.nick != after.nick:
        embed = discord.Embed(
            description=f'🔄 {after.mention} 님의 별명이 변경되었습니다.',
            timestamp=datetime.utcnow(),
            colour=discord.Color.dark_blue()
        )
        embed.set_author(name=after, icon_url=after.avatar_url)
        embed.add_field(name="변경 전", value=(before.nick if before.nick else after.name), inline=False)
        embed.add_field(name="변경 후", value=after.nick if after.nick else after.name, inline=False)
        embed.set_footer(text=f'유저 ID: {after.id}')
        await client.get_channel(log_channel).send(embed=embed)

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(656862634754310178)
    notice_channel = client.get_channel(656865311622168619)

    from datetime import datetime
    embed = discord.Embed(
        description=f"[🔗 서버 재참가](https://discord.gg/XTMJH4R)\n\n"
                    f"안녕하세요 {member.mention} 님,\n"
                    f"🎊 **젠민룸** 서버에 오신것을 진심으로 환영합니다! 🎊\n"
                    f"{notice_channel.mention} 한 번씩 꼭 읽어주세요!",
        timestamp=datetime.utcnow(),
        colour=random.choice(colours),
    )
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_footer(text=f"유저 ID: {member.id}")
    embed.set_thumbnail(url=member.guild.icon_url)
    await member.send(embed=embed)
    await welcome_channel.send(member.mention, embed=embed)

@client.event
async def on_member_remove(member):
    bye_channel = client.get_channel(683877918568611854)
    msg = f"👋 잘가요 **{member}** {member.mention} 님, 나중에 또봐요! **ಥ_ಥ** 👋"
    await bye_channel.send(msg)




client.run(access_token)
