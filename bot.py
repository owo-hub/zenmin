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

access_token = os.environ["BOT_TOKEN"]

client = discord.Client()

badword_list = ['섹스', '느금마', '애미', '애비', '장애인', '느금', '보지', '자지', '니애미', 'badwordtest1', 'badwordtest2']
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

youtube_post_channel = 650334329817268264
last_url = []

async def youtubelast(search):
    global last_url
    while not client.is_closed():
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        if not search_results[0] in last_url:
            last_url.append(search_results[0])
            print("New video!: {}".format('http://www.youtube.com/watch?v=' + search_results[0]))
            await client.get_channel(youtube_post_channel).send('http://www.youtube.com/watch?v=' + search_results[0])
        print(last_url)
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print("Bot is ready.")
    print(client.user.name)
    print(client.user.id)
    print("--------------------")

    asyncio.create_task(youtubelast('오버워치 워크샵'))
    await client.change_presence(status=discord.Status.idle)
    # 봇 활동 (type: 0=하는중, 1=트위치 생방송중, 2=듣는중)
    await client.change_presence(activity=discord.Activity(name='오떱아 도와줘', type=2))

@client.event
async def on_message(message):
    admins = [524980170554212363, 252302363052867587, 276689714592088064, 533859758583840779]
    welcome_channel = client.get_channel(564454482608390155)
    notice_channel = client.get_channel(679540094012882954)
    botcmd_channel = client.get_channel(650340295061536769)
    badword_log_channel = client.get_channel(672192045649231885)
    owohub_id = client.get_guild(539446073320669185)

    if any(x in message.content for x in badword_list) and message.guild == owohub_id:
        for badword in badword_list:
            if badword in message.content:
                badwords.append(badword)
        print(badwords)
        from datetime import datetime
        embed = discord.Embed(
            description="{0}님이 {1} **채널에서 욕설을 사용했습니다.**".format(message.author.mention, message.channel.mention),
            timestamp=datetime.utcnow(),
            colour=discord.Colour.red()
        )
        embed.set_author(name=message.author,
                         icon_url=message.author.avatar_url)
        embed.add_field(name="제거된 메시지", value=message.content)
        embed.add_field(name="감지된 욕설 ({0})".format(len(badwords)), value=", ".join(str(i) for i in badwords), inline=False)
        embed.set_footer(text="ID: {0}".format(message.author.id))
        await message.delete()
        await badword_log_channel.send(embed=embed)

    # 개인 메시지
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        # 받은 DM을 포스팅할 채널
        dm_channels = [672192045649231885]
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

        if message.content.startswith('오떱아 말해 '):
            msg = message.content[7:]
            await message.delete()
            await message.channel.send(msg)

        if message.content.startswith('오떱아 읽어 '):
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
    if message.content.startswith("오떱아 도와줘"):
        from datetime import datetime
        embed = discord.Embed(
            title='저를 부를 땐 앞에 "오떱아"를 붙여주세요!',
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green()
        )
        embed.set_author(name='OWOHUB Bot Commands', icon_url=message.guild.icon_url)
        embed.set_thumbnail(url=message.guild.icon_url)
        embed.add_field(name="관리자 명령어", value="`말해`, `읽어`", inline=False)
        embed.add_field(name="유저 명령어", value="`도와줘`, `안녕`, `멤버수`, `관리자`, `영웅추천`, `노래틀어줘`, `고마워`, `배너볼래`, `배너안볼래`", inline=False)
        embed.add_field(name="검색 명령어", value="`누구야`, `유튜브`, `배틀태그`", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("오떱아 안녕"):
        await message.channel.send("안녕하세요, {.mention}님 !".format(message.author))

    if message.content.startswith("오떱아 누구야 "):
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

    if message.content.startswith("오떱아 노래틀어줘"):
        from datetime import datetime
        date = datetime.now()
        await message.channel.send(";;p 멜론차트 {0}월 {1}일".format(str(date.month), str(date.day)))
        await asyncio.sleep(1)
        # await message.channel.send("인식이 안댕..")
        await message.channel.send("{0} 죄송해요 저는 아직 노래를 틀을수 없어요!!!".format(message.author.mention))

    if message.content.startswith("오떱아 고마워"):
        thankmsg = ["헤헿", "^^", " (っ˘ڡ˘ς) ", "{0} 저도 고마워요!".format(message.author.mention), "응"]
        await message.channel.send(random.choice(thankmsg))

    if message.content.startswith("오떱아 멤버수"):
        await message.channel.send(f"현재 **{message.guild.name}** 서버에는 **{message.guild.member_count}**명이 있어요!")

    if message.content.startswith("오떱아 관리자"):
        await message.channel.send(", ".join(str(message.guild.get_member(i)) for i in admins))

    if message.content.startswith("오떱아 영웅추천"):
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

    if message.content.startswith("오떱아 유튜브 "):
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
        await message.channel.send('{0}중 {1}\n'.format(len(search_results), randomNum) + 'http://www.youtube.com/watch?v=' + search_results[randomNum])

    if message.content.startswith("오떱아 워크샵"):
        query_string = urllib.parse.urlencode({
            'search_query': '오버워치 워크샵'
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        await message.channel.send('http://www.youtube.com/watch?v=' + search_results[0])

    if message.content.startswith("오떱아 배틀태그 "):
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

    if message.content.startswith("오떱아 opgg "):
        tag = message.content[9:]
        battletag = tag.replace("#", "%23")
        print(tag + " to " + battletag)
        url = 'https://overwatch.op.gg/search/?playerName=' + battletag
        url = urllib.parse.urlsplit(url)
        url = list(url)
        print(url)
        url[2] = urllib.parse.quote(url[2])
        profile_url = urllib.parse.urlunsplit(url)
        print(profile_url)
        htm_content = urllib.request.urlopen(profile_url).read()
        htm_content = str(htm_content)
        profile_img = re.findall(r'<div class="ProfileImage"> <div> <img src="(https://.*?png)"', htm_content)
        print(profile_img)

    if message.content.startswith("오떱아 서버정보"):
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

    if message.content.startswith("오떱아 입장테스트"):
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

    if message.content.startswith("오떱아 배너안볼래"):
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

    if message.content.startswith("오떱아 배너볼래"):
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

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(564454482608390155)
    notice_channel = client.get_channel(679540094012882954)
    botcmd_channel = client.get_channel(650340295061536769)

    from datetime import datetime
    embed = discord.Embed(
        title="🔗 서버 재참가 링크",
        description=f"Hey! {member.mention},",
        timestamp=datetime.utcnow(),
        colour=random.choice(colours),
        url="https://discordapp.com/invite/E2PsZwH"
    )
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_footer(text=f"유저 ID: {member.id}")
    # embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(
        name=f"Welcome to the **Overwatch Workshop** Community **OWOHUB** Server !",
        value=f"**오버워치 워크샵** 커뮤니티 **오떱헙** 서버에 오신것을 진심으로 환영합니다! 🎊"
    )
    embed.add_field(
        name=f"Don't forget to read the **annoucement**!",
        value=f"가끔 올라오는 공지사항 {notice_channel.mention}, 꼭 잊지 말고 읽어주세요!",
        inline=False
    )
    await member.send(embed=embed)
    await welcome_channel.send(member.mention, embed=embed)

@client.event
async def on_member_remove(member):
    bye_channel = client.get_channel(675121336271503361)
    msg = f"👋 잘가요 {member} {member.mention}님, 나중에 또봐요! `ಥ_ಥ`"
    await bye_channel.send(msg)

client.run(access_token)
