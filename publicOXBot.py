import datetime
import time

import discord
from discord import Colour
from discord.ext import tasks
from konlpy.tag import Okt

# 별도 파일들
import Calculator
import NewMinigame as Mini
import OX_Quiz_Result
import Offer_Process_Time
import get_Boss
import get_ranking
import minigamenoticeservice
import publicJudgeBan
import public_query

# 메콩OX봇#5381

client = discord.Client()

# BOT Token
# Main Token = "{DISCORD_BOT_TOKEN}"
token = "{DISCORD_BOT_TOKEN}"


# Dev Token
token = "{DISCORD_BOT_TOKEN}"


# Bot initialize
@client.event
# 처음 켰을 때 호출되는 함수
async def on_connect():
    nlpy = Okt()
    nlpy.nouns("옵치")
    print("nlpy Load")


# 1초에 한번 수행될 작업
# 여기 함수는 에러가 나도 에러 메시지가 출력되지 않으므로 주의.
@tasks.loop(seconds=1)
async def send_minigame_message():
    # 미니게임은 5분 또는 35분이므로, 0분, 30분 0초에만 함수가 작동되도록 정의
    if datetime.datetime.now().second == 0 and (
            datetime.datetime.now().minute == 0 or datetime.datetime.now().minute == 30):
        try:
            subscriber = minigamenoticeservice.get_subscriber()
            msg = Mini.get_recent_minigame()

            for i in subscriber[0]:
                try:
                    guild_channel = client.get_guild(int(i[0])).get_channel(int(i[1]))

                    if str(msg['status']) == 'success':
                        await guild_channel.send(embed=msg['message'], delete_after=60.0)

                except Exception as e:
                    minigamenoticeservice.error_handling(i[0], "Server")

            for i in subscriber[1]:
                try:
                    dm_channel = await client.get_user(int(i)).create_dm()

                    if str(msg['status']) == 'success':
                        await dm_channel.send(embed=msg['message'])

                except Exception as e:
                    minigamenoticeservice.error_handling(i, "DM")

            # 1초 sleep하여 중복 전송 방지
            time.sleep(1)

        except Exception as e:
            print(e)


@client.event
# on_ready는 봇을 다시 구성할 때도 호출 됨 (한번만 호출되는 것이 아님.)
async def on_ready():
    game = discord.Game("!설명서, !ox로 검색")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("READY")

    send_minigame_message.start()


# message respond
@client.event
async def on_message(message):
    start = time.time()
    channel = message.channel

    # sender가 bot일 경우 ignore
    if message.author.bot:
        return None

    # 미니게임 알림 서비스
    if message.content == '!알림설명':
        if publicJudgeBan.judge(message):
            return None

        embed = discord.Embed(title="미니게임 5분 전 알림 등록 방법", description="  ", color=0x00ff56)
        embed.add_field(name="설정하는 명령어", value="\'!알림설정 (시작 시간) (끝 시간)\'으로 설정", inline=False)
        embed.add_field(name="서버에 알림을 전하고 싶은 경우", value="서버의 관리자가 전달 받기 원하는 채널에서 명령을 등록하세요.", inline=False)
        embed.add_field(name="DM으로 전달받고 싶은 경우", value="봇에게 DM을 보내서 위의 명령을 등록하세요", inline=False)
        embed.add_field(name="시간 입력 요령", value="24시간제를 기준으로 작성하셔야합니다.", inline=False)
        embed.add_field(name="알림을 삭제하고 싶은 경우", value="\'!알림삭제\'", inline=False)
        embed.add_field(name="시간을 바꾸고 싶은 경우", value="위의 명령어를 입력하시면 자동으로 인식하고 변경처리합니다.", inline=False)
        embed.add_field(name="예시", value="!알림설정 17 21 -> 17시 ~ 21시 59분까지 미니게임 시작 5분 전에 알림을 받습니다.", inline=False)
        embed.set_footer(text="* 오전 6시에는 서버 재구동 시간이므로 작동되지 않습니다. 양해 부탁 드립니다.")
        await channel.send(embed=embed, delete_after=60.0)
        return None

    # 미니게임 알림 서비스 등록
    if message.content.startswith('!알림설정'):
        if publicJudgeBan.judge(message):
            return None

        await channel.send(minigamenoticeservice.register_service(message), delete_after=10.0)
        return None

    # 미니게임 알림 서비스 삭제
    if message.content.startswith('!알림삭제'):
        if publicJudgeBan.judge(message):
            return None

        await channel.send(minigamenoticeservice.delete_alarm(message), delete_after=10.0)
        return None

    if message.content == '!ox' or message.content == '!OX':
        if publicJudgeBan.judge(message):
            return None

        msg = "입력한 키워드가 없습니다."
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=10.0)
        public_query.log_upload(message, "ox", msg, str(time.time() - start))
        return None

    if message.content.startswith("!연산 "):
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

        nlpy = Okt()

        msg = OX_Quiz_Result.get(message, "Public", nlpy)
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        # user, type, chat, respond
        public_query.log_upload(message, "ox", msg, str(time.time() - start))
        return None

    if message.content.startswith('!ㅋ ') or message.content.startswith('!q '):
        channel = message.channel

        # 허용된 서버에서 사용하는지 확인
        try:
            if (not str(message.guild.id) == "{DISCORD_SERVER_ID}") and (not str(message.guild.id) == "{DISCORD_SERVER_ID}"):
                return None
        # DM인 경우
        except AttributeError:
            return None

        # 형태소 분석기 로드
        nlpy = Okt()

        msg = OX_Quiz_Result.get(message, "Public", nlpy)
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg)
        public_query.log_upload(message, "ox", msg, str(time.time() - start))
        return None

    # 필보 검색
    if message.content.startswith("!필보"):
        if publicJudgeBan.judge(message):
            return None

        msg = get_Boss.get(message, "Public")
        msg = Offer_Process_Time.configure(start, msg, message)
        await channel.send(msg, delete_after=60.0)
        public_query.log_upload(message, "boss", msg, str(time.time() - start))
        return None

    # 미니게임 시간표
    if message.content == "!미겜":
        if publicJudgeBan.judge(message):
            return None

        msg = Mini.get_recent_minigame()

        if str(msg['status']) == 'success':
            await channel.send(Offer_Process_Time.configure(start, "", message), embed=msg['message'],
                               delete_after=60.0)
            public_query.log_upload(message, "Minigame", msg['log'], str(time.time() - start))
            return None
        else:
            msg['message'] += Offer_Process_Time.configure(start, msg['message'], message)
            await channel.send(msg['message'], delete_after=60.0)
            public_query.log_upload(message, "Minigame", msg['message'], str(time.time() - start))
            return None

    # 다음 미니게임 시간표
    if message.content == "!다음미겜":
        if publicJudgeBan.judge(message):
            return None

        msg = Mini.get_next_minigame()

        if str(msg['status']) == 'success':
            await channel.send(Offer_Process_Time.configure(start, "", message), embed=msg['message'],
                               delete_after=60.0)
            public_query.log_upload(message, "Minigame", msg['log'], str(time.time() - start))
            return None
        else:
            msg['message'] += Offer_Process_Time.configure(start, msg['message'], message)
            await channel.send(msg['message'], delete_after=60.0)
            public_query.log_upload(message, "Minigame", msg['message'], str(time.time() - start))
            return None

    # 길드 트로피 1페이지 순위를 요청한 경우
    if message.content == "!길트" or message.content == "!길트 " or message.content == "!길트종 " or message.content == "!길트종":
        channel = message.channel

        # 허용된 서버에서 사용하는지 확인
        try:
            if (not str(message.guild.id) == "{DISCORD_SERVER_ID}") and (not str(message.guild.id) == "{DISCORD_SERVER_ID}"):
                return None
        # DM인 경우
        except AttributeError:
            return None

        # 실시간 순위를 요청한 경우
        if message.content == "!길트" or message.content == "!길트 ":
            # 결과를 구해옴
            result = get_ranking.get_guild_ranking("realtime")
        # 종합 순위를 요청한 경우
        else:
            # 결과를 구해옴
            result = get_ranking.get_guild_ranking("None")

        # 받은 결과를 토대로 메시지 전달
        result['msg'] = Offer_Process_Time.configure(start, result['msg'], message)

        # 종합 순위인 경우 알림 메시지 추가
        if message.content == "!길트종 " or message.content == "!길트종":
            result['msg'] = "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-\n" + result['msg']
            await channel.send(result['msg'])
        else:
            await channel.send(result['msg'])

        if str(result['status']) == "success":
            public_query.log_upload(message, "길트", result['msg'], str(time.time() - start))
        elif str(result['status']) == "error":
            public_query.log_upload(message, "길트(error)", result['msg'], str(time.time() - start))

        return None

    # 특정 길드의 순위를 확인하는 경우
    if message.content.startswith("!길트 ") or message.content.startswith("!길트종 "):
        channel = message.channel

        # 허용된 서버에서 사용하는지 확인
        try:
            if (not str(message.guild.id) == "{DISCORD_SERVER_ID}") and (not str(message.guild.id) == "{DISCORD_SERVER_ID}"):
                return None
        # DM인 경우
        except AttributeError:
            return None

        # 실시간 순위를 원하는 경우
        if message.content.startswith("!길트 "):
            # 순위를 가져옴
            result = get_ranking.get_guild_ranking_search_by_keyword("realtime", message.content.replace("!길트 ", "", 1))
        # 종합 순위를 요청하는 경우
        else:
            # 결과를 갖고 옴
            result = get_ranking.get_guild_ranking_search_by_keyword("None",
                                                                     message.content.replace("!길트종 ", "", 1))

        # 에러가 발생한 경우
        if str(result['status']) == "error":
            result['msg'] = Offer_Process_Time.configure(start, result['msg'], message)
            await channel.send(result['msg'])
            public_query.log_upload(message, "길트(error)", result['msg'], str(time.time() - start))
            return None

        file = discord.File(result['name'] + ".png", filename="guildimage.png")

        line_color = Colour.from_rgb(result['r'], result['g'], result['b'])

        # 에러가 아닌 경우 제대로 받아온 것이므로 결과를 기반으로 메시지 구성
        embed = discord.Embed(title="길드 검색 결과", description="  ", color=line_color)
        embed.set_thumbnail(url="attachment://guildimage.png")
        embed.add_field(name="이름", value=str(result['name']), inline=True)
        embed.add_field(name="순위", value=str(result['rank']) + "위", inline=True)
        embed.add_field(name="길드장", value=str(result['leader']), inline=True)
        embed.add_field(name="길드 트로피", value=str(result['trop']) + "개", inline=True)

        # 종합 순위를 요청한 경우
        if message.content.startswith("!길트종 "):
            await channel.send("-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-" +
                               Offer_Process_Time.configure(start, "", message), embed=embed, file=file)
        else:
            await channel.send(Offer_Process_Time.configure(start, "", message), embed=embed, file=file)

        return None

    # 개인 트로피 순위 1페이지를 요청한 경우
    if message.content == "!개트" or message.content == "!개트 " or message.content == "!개트종" or message.content == "!개트종 ":
        channel = message.channel

        # 허용된 서버에서 사용하는지 확인
        try:
            if not str(message.guild.id) == "{DISCORD_SERVER_ID}" or not str(message.guild.id) == "{DISCORD_SERVER_ID}":
                return None
        # DM인 경우
        except AttributeError:
            return None

        # 실시간 순위를 요구한 경우
        if message.content == "!개트" or message.content == "!개트 ":
            result = get_ranking.get_person_ranking("realtime")
        # 종합 순위를 요구한 경우
        else:
            result = get_ranking.get_person_ranking("None")

        result['msg'] = Offer_Process_Time.configure(start, result['msg'], message)

        # 종합 순위를 요구한 경우
        if message.content == "!개트종" or message.content == "!개트종 ":
            result['msg'] = "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-" + result['msg']
            # 메시지 전송
            await channel.send(result['msg'])
        # 실시간 순위를 요구한 경우
        else:
            # 메시지 전송
            await channel.send(result['msg'])

        if str(result['status']) == "success":
            public_query.log_upload(message, "개트", result['msg'], str(time.time() - start))
        elif str(result['status']) == "error":
            public_query.log_upload(message, "개트(error)", result['msg'], str(time.time() - start))

        return None

    # 특정 캐릭터의 순위를 요구한 경우
    if message.content.startswith("!개트 ") or message.content.startswith("!개트종 "):
        channel = message.channel

        # 허용된 서버에서 사용하는지 확인
        try:
            if (not str(message.guild.id) == "{DISCORD_SERVER_ID}") and (not str(message.guild.id) == "{DISCORD_SERVER_ID}"):
                return None
        # DM인 경우
        except AttributeError:
            return None

        # 실시간 순위를 원하는 경우
        if message.content.startswith("!개트 "):
            # 순위를 가져옴
            result = get_ranking.get_person_ranking_search_by_keyword("realtime",
                                                                      message.content.replace("!개트 ", "", 1))
        # 종합 순위를 요청하는 경우
        else:
            # 결과를 갖고 옴
            result = get_ranking.get_person_ranking_search_by_keyword("None",
                                                                      message.content.replace("!개트종 ", "", 1))

        # 에러가 발생한 경우
        if str(result['status']) == "error":
            result['msg'] = Offer_Process_Time.configure(start, result['msg'], message)
            await channel.send(result['msg'])
            public_query.log_upload(message, "개트(error)", result['msg'], str(time.time() - start))
            return None

        file = discord.File(result['nickname'] + ".png", filename="profileimage.png")

        # 에러가 아닌 경우 제대로 받아온 것이므로 결과를 기반으로 메시지 구성
        line_color = Colour.from_rgb(result['r'], result['g'], result['b'])

        embed = discord.Embed(title="캐릭터 검색 결과", description="  ", color=line_color)
        embed.set_thumbnail(url="attachment://profileimage.png")
        embed.add_field(name="닉네임", value=str(result['nickname']), inline=True)
        embed.add_field(name="순위", value=str(result['rank']) + "위", inline=True)
        embed.add_field(name="트로피", value=str(result['trop']) + "개", inline=True)

        # 종합 순위를 요청한 경우
        if message.content.startswith("!개트종 "):
            if result['num'] > 1:
                await channel.send("검색 결과에 닉네임이 중복된 캐릭터가 발견되었습니다. 트로피가 제일 많은 캐릭터를 표시합니다.\n"
                                   "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-" +
                                   Offer_Process_Time.configure(start, "", message), embed=embed, file=file)
            else:
                await channel.send("-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-" +
                                   Offer_Process_Time.configure(start, "", message), embed=embed, file=file)
        else:
            if result['num'] > 1:
                await channel.send("검색 결과에 닉네임이 중복된 캐릭터가 발견되었습니다. 트로피가 제일 많은 캐릭터를 표시합니다." +
                                   Offer_Process_Time.configure(start, "", message), embed=embed, file=file)
            else:
                await channel.send(Offer_Process_Time.configure(start, "", message), embed=embed, file=file)

        return None

    # 커스텀 메시지
    if message.content.startswith("!"):
        if publicJudgeBan.judge(message):
            return None

        try:
            if str(message.guild.id) == "{DISCORD_SERVER_ID}" or str(message.guild.id) == "{DISCORD_SERVER_ID}":
                msg = public_query.get_custom_query(message, 1)
            else:
                msg = public_query.get_custom_query(message, 0)
        except AttributeError:
            msg = public_query.get_custom_query(message, 0)

        if not msg == "False":
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg, delete_after=60.0)
            public_query.log_upload(message, "CustomRespond", msg, str(time.time() - start))
            return None
        else:
            return None

client.run(token)
