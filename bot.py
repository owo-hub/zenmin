import discord
from discord.ext import commands
import datetime
import os
import random
import asyncio

access_token = os.environ["BOT_TOKEN"]

client = discord.Client()

log_channel = 683877528494014464
notice_channel = 656865311622168619

@client.event
async def on_ready():
    print("Bot is ready.")
    print(client.user.name)
    print(client.user.id)
    print("--------------------")
    await client.change_presence(activity=discord.Streaming(platform='Twitch', name='젠민아 도와줘', url='https://www.twitch.tv/zenmin_ow/'))
    from datetime import datetime
    check = await client.get_channel(684157506972549159).send(embed=discord.Embed(description=f"🚨 젠민님을 좋아해서 이서버에 오셨습니까? 🚨\n{client.get_channel(notice_channel).mention} 꼭 확인하시고 선택해 주세요.", timestamp=datetime.utcnow(), colour=discord.Color.teal()))
    await check.add_reaction(emoji='✅')
    await check.add_reaction(emoji='❌')

@client.event
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
            await user.add_roles(cross_role)
                                 
client.run(access_token)
