import re
import time
import urllib.request

import discord

# 별도 파일들
import Mini
import get_ranking
import publicJudgeBan
import public_query

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
    game = discord.Game("새 기능이 있어요. !설명서")
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

    # 길드 트로피 순위
    if message.content == "!길트" or message.content == "!길트 ":
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel

        msg = get_ranking.get_guild_ranking("realtime")
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "Ranking", msg)
        return None

    # 길드 트로피 순위 검색
    if message.content.startswith("!길트 "):
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel

        keyword = message.content.replace("!길트 ", "", 1)
        guild_list = get_ranking.get_guild_ranking_search_by_keyword("realtime", keyword)

        if str(type(guild_list)) == "<class 'str'>":
            msg = guild_list
            await channel.send(msg, delete_after=60.0)
            public_query.log_upload(message, "Ranking", msg)
            return None

        urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
        await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

        msg = guild_list[0]['guildmsg']
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "Ranking", msg)
        return None

    # 개인 로피 순위
    if message.content == "!개트" or message.content == "!개트 ":
        if publicJudgeBan.judge(message):
            return None
        channel = message.channel

        msg = get_ranking.get_person_ranking("realtime")
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "Ranking", msg)
        return None

    # 개인 트로피 순위 검색
    if message.content.startswith("!개트 "):
        if publicJudgeBan.judge(message):
            return None
        channel = message.channel

        keyword = message.content.replace("!개트 ", "", 1)
        person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

        if str(type(person_list)) == "<class 'str'>":
            msg = person_list
            await channel.send(msg, delete_after=60.0)
            public_query.log_upload(message, "Ranking", msg)
            return None

        urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
        await channel.send(file=discord.File(person_list[0]['name'] + ".png"), delete_after=60.0)

        msg = person_list[0]['personmsg']
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "Ranking", msg)
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

