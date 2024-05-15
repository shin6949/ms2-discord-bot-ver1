import threading
import time
from pprint import pprint

import discord
import schedule
from discord import Colour
from konlpy.tag import Okt

# 별도 파일
import Calculator
import Morning_Task
import NewMinigame as Mini
import OX_Quiz_Result
import Offer_Process_Time
import Write_error_log
import get_Boss
import get_ranking
import guild_query
import public_query


# 메콩OX봇#5381


def return_location():
    return "GuildOXBot - OXBot.py"


def judge_server(message):
    try:
        if not str(message.guild.id) == "{DISCORD_SERVER_ID}" and not str(message.guild.id) == "{DISCORD_SERVER_ID}":
            msg = "이 봇은 지정된 서버에서만 사용하실 수 있습니다."
            return msg
        else:
            return "True"

    except:
        msg = "이 봇은 DM 모드로는 사용하실 수 없습니다."
        return msg


class chatbot(discord.Client):
    # 처음 켰을 때 호출되는 함수
    async def on_connect(self):
        nlpy = Okt()
        nlpy.nouns("옵치")
        print("nlpy Load")

        # 봇 시작 통보
        msg = "봇이 시작되었습니다.\n사용중인 서버: {}개".format(len(client.guilds))
        # DM으로 전달
        cocoblue = await client.get_user({DEVELOPER_USER_ID}).create_dm()
        await cocoblue.send(msg)

    # on_ready는 봇을 다시 구성할 때도 호출 됨 (한번만 호출되는 것이 아님.)
    async def on_ready(self):
        game = discord.Game("!설명서, !ㅋ으로 문제 검색")
        await client.change_presence(status=discord.Status.online, activity=game)
        print("READY")

    # {PRIVATE_GUILD_NAME} 길드 서버 ID: {DISCORD_SERVER_ID}
    # {PRIVATE_GUILD_NAME} 길드 내 자유 채팅 채널 ID: {PRIVATE_DISCORD_CHANNEL_ID}
    # TEST 서버 내 자유 채팅 채널 ID: {TEST_DISCORD_CHANNEL_ID}
    async def on_member_join(self, member):
        # 입장한 계정이 봇인 경우 어떠한 이벤트도 실행하지 않음.
        if member.bot:
            return None

        # {PRIVATE_GUILD_NAME} 길드 서버 ID 라면
        if str(member.guild.id) == "{DISCORD_SERVER_ID}":
            # {SERVER_ADMIN_NAME}({SERVER_ADMIN_ID}), {SERVER_ADMIN_NAME}({SERVER_ADMIN_ID}) 자동 태그
            msg = "'<@{}>'님이 서버에 들어오셨어요. 환영합니다." \
                  "\n인게임 닉네임을 말씀하시면 확인 후 닉네임 변경해드립니다. 그렇죠 <@{}>, <@{}>님?" \
                .format(str(member.id), str({SERVER_ADMIN_ID}), str({SERVER_ADMIN_ID}))
            await member.guild.get_channel({PRIVATE_DISCORD_CHANNEL_ID}).send(msg)

        # 테스트 서버 ID 라면
        else:
            msg = "'<@{}>'님이 서버에 들어오셨어요. 환영합니다.".format(member.id)
            await member.guild.get_channel({TEST_DISCORD_CHANNEL_ID}).send(msg)
            return None

    async def on_member_update(self, before, after):
        # {PRIVATE_GUILD_NAME} 길드 서버 ID 라면
        if str(after.guild.id) == "{DISCORD_SERVER_ID}":
            channel = after.guild.get_channel({PRIVATE_DISCORD_CHANNEL_ID})
        # 테스트 서버 ID 라면
        else:
            channel = after.guild.get_channel({TEST_DISCORD_CHANNEL_ID})

        if not before.nick == after.nick:
            if before.nick is None:
                if after.nick is None:
                    msg = "<@{}> '{}'님에서 '{}'님으로 닉네임이 변경되었습니다.".format(after.id, before.name, after.name)
                else:
                    msg = "<@{}> '{}'님에서 '{}'님으로 닉네임이 변경되었습니다.".format(after.id, before.name, after.nick)
            elif after.nick is None:
                msg = "<@{}> '{}'님에서 '{}'님으로 닉네임이 변경되었습니다.".format(after.id, before.nick, after.name)
            else:
                msg = "<@{}> '{}'님에서 '{}'님으로 닉네임이 변경되었습니다.".format(after.id, before.nick, after.nick)

            await channel.send(msg)
            return None

    async def on_message(self, message):
        # 연산 시작 시간 저장
        start = time.time()

        # sender가 bot일 경우 아무 반응도 하지 않음.
        if message.author.bot:
            return None

        # 계산기 기능
        if message.content.startswith("!연산 "):
            channel = message.channel
            judge = judge_server(message)

            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = Calculator.cal(message, "Guild")
            msg = Offer_Process_Time.configure(start, msg, message)

            await channel.send(msg)
            public_query.log_upload(message, "calculator", msg['message'], str(time.time() - start))
            return None

        # 미니게임 시간표
        if message.content == "!미겜":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = Mini.get_recent_minigame()

            if str(msg['status']) == 'success':
                await channel.send(Offer_Process_Time.configure(start, "", message), embed=msg['message'])
                public_query.log_upload(message, "Minigame", msg['log'], str(time.time() - start))
                return None
            else:
                msg['message'] += Offer_Process_Time.configure(start, msg['message'], message)
                await channel.send(msg['message'])
                public_query.log_upload(message, "Minigame", msg['message'], str(time.time() - start))
                return None

        # 다음 미니게임 시간표
        if message.content == "!다음미겜":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = Mini.get_next_minigame()
            if str(msg['status']) == 'success':
                await channel.send(Offer_Process_Time.configure(start, "", message), embed=msg['message'])
                public_query.log_upload(message, "Minigame", msg['log'], str(time.time() - start))
                return None
            else:
                msg['message'] += Offer_Process_Time.configure(start, msg['message'], message)
                await channel.send(msg['message'])
                public_query.log_upload(message, "Minigame", msg['message'], str(time.time() - start))
                return None

        # OX 퀴즈 검색하기 -> 입력한 키워드가 없는 경우
        if message.content == '!ox' or message.content == '!OX' or message.content == '!퀴즈' or message.content == '!ㅋ' or message.content == '!q':
            channel = message.channel
            msg = "입력한 키워드가 없습니다!!"
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)

            return None

        # OX 퀴즈 검색하기 -> 입력한 키워드가 있는 경우
        if message.content.startswith('!ox ') or message.content.startswith('!OX ') or message.content.startswith(
                '!퀴즈 ') or message.content.startswith('!ㅋ ') or message.content.startswith('!q '):
            # 형태소 분석기 로드
            nlpy = Okt()

            channel = message.channel

            # 허용된 서버에서 사용하는지 확인
            judge = judge_server(message)

            # 허용되지 않은 서버에서 사용하는 경우 사용 불가 메시지를 전달
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = OX_Quiz_Result.get(message, "Guild", nlpy)
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            public_query.log_upload(message, "ox", msg, str(time.time() - start))
            return None

        # 필보 검색
        if message.content.startswith("!필보"):
            channel = message.channel

            # 허용된 서버에서 사용하는지 확인
            judge = judge_server(message)

            # 허용되지 않은 서버에서 사용하는 경우 사용 불가 메시지를 전달
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = get_Boss.get(message, "Guild")
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            public_query.log_upload(message, "boss", msg, str(time.time() - start))
            return None

        # 길드 트로피 1페이지 순위를 요청한 경우
        if message.content == "!길트" or message.content == "!길트 " or message.content == "!길트종 " or message.content == "!길트종":
            channel = message.channel

            # 허용된 서버에서 사용하는지 확인
            judge = judge_server(message)

            # 허용되지 않은 서버에서 사용하는 경우 사용 불가 메시지를 전달
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
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
            judge = judge_server(message)

            # 허용되지 않은 서버에서 사용하는 경우 사용 불가 메시지를 전달
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            # 실시간 순위를 원하는 경우
            if message.content.startswith("!길트 "):
                # 순위를 가져옴
                result = get_ranking.get_guild_ranking_search_by_keyword("realtime",
                                                                         message.content.replace("!길트 ", "", 1))
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
            judge = judge_server(message)

            # 허용되지 않은 서버에서 사용하는 경우 사용 불가 메시지를 전달
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
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
            judge = judge_server(message)

            # 허용되지 않은 서버에서 사용하는 경우 사용 불가 메시지를 전달
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
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
            line_color = Colour.from_rgb(result['r'], result['g'], result['b'])

            # 에러가 아닌 경우 제대로 받아온 것이므로 결과를 기반으로 메시지 구성
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

        # 커스텀 쿼리
        if message.content.startswith("!"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = guild_query.get_custom_query(message)

            if not msg == "False":
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None
            else:
                return None


def thread_execute():
    schedule.every().day.at("05:00").do(doing_task).tag("SQL TASK")
    pprint(schedule.jobs)
    Write_error_log.write_log(return_location(), "Task Scheduled")

    while True:
        schedule.run_pending()
        time.sleep(1)


def doing_task():
    if Morning_Task.doing_task():
        Write_error_log.write_log(return_location(), "Morning Task Finished")
    else:
        Write_error_log.write_log(return_location(), "Morning Task Failed")


if __name__ == "__main__":
    client = chatbot(max_messages=None)
    thread_1 = threading.Thread(target=thread_execute)
    thread_1.start()

    Write_error_log.write_log(return_location(), "Thread Start")

    # BOT Token
    # Main Token = "{DISCROD_BOT_TOKEN}"
    token = "{DISCROD_BOT_TOKEN}"

    # Dev Token = "{DISCORD_BOT}"
    # token = "{DISCORD_BOT}"
    client.run(token)
