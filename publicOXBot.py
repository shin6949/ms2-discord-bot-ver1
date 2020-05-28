import time
from konlpy.tag import Okt
import discord

# 별도 파일들
import Calculator
import Mini
import testing_ox_query as OX_Quiz_Result
import Offer_Process_Time
import get_Boss
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
# 처음 켰을 때 호출되는 함수
async def on_connect(self):
    nlpy = Okt(max_heap_size=79)
    nlpy.nouns("옵치")
    print("nlpy Load")


# on_ready는 봇을 다시 구성할 때도 호출 됨 (한번만 호출되는 것이 아님.)
async def on_ready():
    game = discord.Game("!ox로 검색, !설명서")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("READY")


# message respond
@client.event
async def on_message(message):
    start = time.time()
    # sender가 bot일 경우 ignore
    if message.author.bot:
        return None

    if message.content == '!ox' or message.content == '!OX':
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel
        msg = "입력한 키워드가 없습니다."
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=10.0)
        public_query.log_upload(message, "ox", msg, str(time.time() - start))
        return None

    if message.content.startswith("!연산 "):
        channel = message.channel

        if publicJudgeBan.judge(message):
            return None

        msg = Calculator.cal(message, "Public")
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "calculator", msg, str(time.time() - start))
        return None

    # OX 퀴즈 검색하기
    if message.content.startswith('!ox ') or message.content.startswith('!OX '):
        if publicJudgeBan.judge(message):
            return None
        channel = message.channel
        nlpy = Okt(max_heap_size=79)

        msg = OX_Quiz_Result.get(message, "Public", nlpy)
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        # user, type, chat, respond
        public_query.log_upload(message, "ox", msg, str(time.time() - start))
        return None

    # 필보 검색
    if message.content.startswith("!필보"):
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel

        msg = get_Boss.get(message, "Public")
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "boss", msg, str(time.time() - start))
        return None

    # 미니게임 시간표
    if message.content == "!미겜":
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel

        msg = Mini.get_recent_minigame()
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "Minigame", msg, str(time.time() - start))
        return None

    # 다음 미니게임 시간표
    if message.content == "!다음미겜":
        channel = message.channel
        if publicJudgeBan.judge(message):
            return None

        msg = Mini.get_next_minigame()
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        return None

    # 커스텀 메시지
    if message.content.startswith("!"):
        if publicJudgeBan.judge(message):
            return None

        channel = message.channel
        msg = public_query.get_custom_query(message)

        if not msg == "False":
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg, delete_after=60.0)
            public_query.log_upload(message, "CustomRespond", msg, str(time.time() - start))
            return None
        else:
            return None


client.run(token)
