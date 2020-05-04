import threading
import time
import urllib.request
from pprint import pprint
import discord
import schedule
import Backup_Task
import Calculator

# 별도 파일
import Mini
import OX_Quiz_Result
import Offer_Process_Time
import Write_error_log
import get_Boss
import get_ranking
import guild_query


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
    async def on_ready(self):
        game = discord.Game("!설명서, !ㅋ으로 문제 검색")
        await client.change_presence(status=discord.Status.online, activity=game)
        print("READY")

    # {PRIVATE_GUILD_NAME} 길드 서버 ID: {DISCORD_SERVER_ID}
    # {PRIVATE_GUILD_NAME} 길드 내 자유 채팅 채널 ID: {PRIVATE_DISCORD_CHANNEL_ID}
    # TEST 서버 내 자유 채팅 채널 ID: {TEST_DISCORD_CHANNEL_ID}
    async def on_member_join(self, member):
        # {PRIVATE_GUILD_NAME} 길드 서버 ID 라면
        if str(member.guild.id) == "{DISCORD_SERVER_ID}":
            channel = member.guild.get_channel({PRIVATE_DISCORD_CHANNEL_ID})
            # {SERVER_ADMIN_NAME}({SERVER_ADMIN_ID}), {SERVER_ADMIN_NAME}({SERVER_ADMIN_ID}) 자동 태그
            msg = "'<@{}>'님이 서버에 들어오셨어요. 환영합니다." \
                  "\n인게임 닉네임을 말씀하시면 확인 후 닉네임 변경해드립니다. 그렇죠 <@{}>, <@{}>님?"\
                .format(str(member.id), str({SERVER_ADMIN_ID}), str({SERVER_ADMIN_ID}))
            await channel.send(msg)
        # 테스트 서버 ID 라면
        else:
            channel = member.guild.get_channel({TEST_DISCORD_CHANNEL_ID})
            msg = "'{}'님이 서버에 들어오셨어요. 환영합니다.".format(member.name)
            await channel.send(msg)

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

    async def on_message(self, message):
        start = time.time()

        # sender가 bot일 경우 ignore
        if message.author.bot:
            return None

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
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            return None

        # OX 퀴즈 검색하기
        if message.content == '!ox' or message.content == '!OX' or message.content == '!퀴즈' or message.content == '!ㅋ' or message.content == '!q':
            channel = message.channel
            msg = "입력한 키워드가 없습니다!!"
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            return None

        if message.content.startswith('!ox ') or message.content.startswith('!OX ') or message.content.startswith(
                '!퀴즈 ') or message.content.startswith('!ㅋ ') or message.content.startswith('!q '):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = OX_Quiz_Result.get(message, "Guild")
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            return None

        # 필보 검색
        if message.content.startswith("!필보"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            msg = get_Boss.get(message, "Guild")
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            return None

        if message.content.startswith("!길트"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            if message.content == "!길트" or message.content == "!길트 ":
                msg = get_ranking.get_guild_ranking("realtime")
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            if message.content == "!길트종" or message.content == "!길트종 ":
                msg = get_ranking.get_guild_ranking("None") \
                      + "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            if not message.content.find("!길트종") == -1:
                keyword = message.content.replace("!길트종 ", "", 1)
                guild_list = get_ranking.get_guild_ranking_search_by_keyword("None", keyword)

                if str(type(guild_list)) == "<class 'str'>":
                    msg = guild_list
                    msg = Offer_Process_Time.configure(start, msg, message)
                    await channel.send(msg)
                    return None

                guild_list[0]['guildmsg'] += "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"

                urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
                await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

                msg = guild_list[0]['guildmsg']
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            keyword = message.content.replace("!길트 ", "", 1)
            guild_list = get_ranking.get_guild_ranking_search_by_keyword("realtime", keyword)

            if str(type(guild_list)) == "<class 'str'>":
                msg = guild_list
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
            await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

            msg = guild_list[0]['guildmsg']
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            return None

        if message.content.startswith("!개트"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                judge = Offer_Process_Time.configure(start, judge, message)
                await channel.send(judge)
                return None

            if message.content == "!개트" or message.content == "!개트 ":
                msg = get_ranking.get_person_ranking("realtime")
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            if message.content == "!개트종" or message.content == "!개트종 ":
                msg = get_ranking.get_person_ranking("None") \
                      + "\n-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            if not message.content.find("!개트종") == -1:
                keyword = message.content.replace("!개트종 ", "", 1)
                person_list = get_ranking.get_person_ranking_search_by_keyword("None", keyword)

                if str(type(person_list)) == "<class 'str'>":
                    msg = person_list
                    msg = Offer_Process_Time.configure(start, msg, message)
                    await channel.send(msg)
                    return None

                person_list[0]['personmsg'] += "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"

                urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
                await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

                msg = person_list[0]['personmsg']
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            keyword = message.content.replace("!개트 ", "", 1)
            person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

            if str(type(person_list)) == "<class 'str'>":
                msg = person_list
                msg = Offer_Process_Time.configure(start, msg, message)
                await channel.send(msg)
                return None

            urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
            await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

            msg = person_list[0]['personmsg']
            msg = Offer_Process_Time.configure(start, msg, message)
            await channel.send(msg)
            return None

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
    schedule.every().day.at("05:00").do(backup_db).tag("SQL TASK")
    pprint(schedule.jobs)
    Write_error_log.write_log(return_location(), "Task Scheduled")

    while True:
        schedule.run_pending()
        time.sleep(1)


def backup_db():
    if Backup_Task.doing_task():
        Write_error_log.write_log(return_location(), "Backup Task Finished")
    else:
        Write_error_log.write_log(return_location(), "Backup Task Failed")


if __name__ == "__main__":
    client = chatbot(max_messages=None)
    thread_1 = threading.Thread(target=thread_execute)
    thread_1.start()

    Write_error_log.write_log(return_location(), "Thread Start")

    # BOT Token
    # Main Token = "{DISCORD_BOT_TOKEN}"
    token = "{DISCORD_BOT_TOKEN}"

    # Dev Token = "{DISCORD_BOT_TOKEN}"
    # token = "{DISCORD_BOT_TOKEN}"
    client.run(token)
