import discord
import time
import re

# 별도 파일들
import Mini
import public_query
import publicJudgeBan

# 메콩OX봇#5381

client = discord.Client()


# BOT Token
# Main Token = "{DISCORD_BOT_TOKEN}"
token = "{DISCORD_BOT_TOKEN}"

# Dev Token
# token = "{DISCORD_BOT_TOKEN}"

# Bot initialize
@client.event
async def on_ready():
    print("READY")
    game = discord.Game("!ox로 문제 검색, !설명서")
    await client.change_presence(status=discord.Status.online, activity=game)


# message respond
@client.event
async def on_message(message):
    # sender가 bot일 경우 ignore
    if message.author.bot:
        return None

    if message.content == '!ox' or message.content == '!OX':
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel
        msg = "입력한 키워드가 없습니다."
        await channel.send(msg, delete_after=10.0)
        public_query.log_upload(message, "ox", msg)
        return None

    # OX 퀴즈 검색하기
    if message.content.startswith('!ox ') or message.content.startswith('!OX '):
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel

        try:
            keyword = message.content.replace("!ox ", "", 1).replace("!OX ", "", 1)

            if len(keyword) < 2:
                msg = "검색어는 2글자 이상 입력해주세요."
                await channel.send(msg, delete_after=10.0)
                public_query.log_upload(message, "ox", msg)
                return None

            msg = public_query.get_query_result(keyword)
            await channel.send(msg, delete_after=60.0)
            # user, type, chat, respond
            public_query.log_upload(message, "ox", msg)
            return None

        except Exception as e:
            print(e)
            return None

    # 필보 검색
    if message.content.startswith("!필보"):
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel
        start = time.time()

        if message.content == "!필보":
            await channel.send("키워드를 입력해주세요. (ex. !필보 5)")
            return None

        keyword = re.findall('\d+', message.content)[0]

        try:
            msg = public_query.get_boss(keyword, message, start)
            await channel.send(msg, delete_after=60.0)
            public_query.log_upload(message, "boss", msg)
            return None

        except Exception as e:
            print(e)
            return None

    # 미니게임 시간표
    if message.content == "!미겜":
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel

        msg = Mini.get_recent_minigame()
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "Minigame", msg)
        return None

    if message.content.startswith("!"):
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel
        msg = public_query.get_custom_query(message)

        if not msg == "False":
            await channel.send(msg, delete_after=60.0)
            public_query.log_upload(message, "CustomRespond", msg)
            return None
        else:
            return None

    if not message.content.find("공군") == -1 or not message.content.find("{PRIVATE_GUILD_NAME}") == -1:
        if message.content.find("공군") > -1:
            public_query.chat_upload(message, "Keyword:공군")
            return None

        if message.content.find("{PRIVATE_GUILD_NAME}") > -1:
            public_query.chat_upload(message, "Keyword:{PRIVATE_GUILD_NAME}")
            return None
    
client.run(token)
