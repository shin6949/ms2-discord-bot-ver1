import re
import time
import urllib.request
import schedule
import discord
from pprint import pprint
import threading

# 별도 ?��?��
import Mini
import get_ranking
import get_tts_mp3
import inner_query
import Backup_Task
import Write_error_log


# 메콩OX�?#5381

def return_location():
    return "GuildOXBot - OXBot.py"


def where_user_in(message):
    user_id = message.author.id
    guild_voice_list = message.guild.voice_channels

    for i in guild_voice_list:
        for j in range(len(i.members)):
            # i 채널?�� ?��??�? ?��?���?
            if str(i.members[j].id) == str(user_id):
                # ?��??�? ?��?�� 보이?�� 채널?�� 리턴
                return i

    return "False"


def judge_server(message):
    try:
        if not str(message.guild.id) == "{DISCORD_SERVER_ID}" and not str(message.guild.id) == "{DISCORD_SERVER_ID}":
            msg = "?�� 봇�? �??��?�� ?��버에?���? ?��?��?��?�� ?�� ?��?��?��?��."
            return msg
        else:
            return "True"

    except:
        msg = "?�� 봇�? DM 모드로는 ?��?��?��?�� ?�� ?��?��?��?��."
        return msg


class chatbot(discord.Client):
    async def on_ready(self):
        game = discord.Game("!?��명서, !?��?���? 문제 �??��")
        await client.change_presence(status=discord.Status.online, activity=game)
        print("READY")

    async def on_message(self, message):
        if message.content.startswith("\"\" "):
            channel = message.channel
            voice_channel = where_user_in(message)

            if voice_channel == "False":
                await channel.send('?��?���? ?��?�� 보이?�� 채널?�� ?��?��?��?��.', delete_after=10.0)
                get_tts_mp3.upload_log(message)
                return None
            else:
                keyword = message.content.replace("\"\" ", "", 1)

                if get_tts_mp3.get_kakao_mp3(message, keyword):
                    try:
                        current_voiceclient = await voice_channel.connect(timeout=3.0)
                        time.sleep(1)
                    except:
                        current_voiceclient = client.voice_clients[0]
                        if not str(voice_channel.name) == str(current_voiceclient.channel):
                            await current_voiceclient.disconnect(force=True)
                            current_voiceclient = await voice_channel.connect(timeout=3.0)

                    mp3url = "result.mp3"
                    try:
                        current_voiceclient.play(discord.FFmpegPCMAudio(mp3url))
                        get_tts_mp3.upload_log(message)
                        return None

                    except:
                        msg = "먼�? ?���??�� 메시�?�? ?��?��?���? ?��?��?��?��."
                        await channel.send(msg, delete_after=10.0)
                        get_tts_mp3.upload_log(message)
                        return None
                else:
                    msg = "?���? 문제�? ?��?�� TTS 구성?�� ?��?��?��???��?��?��."
                    await channel.send(msg, delete_after=10.0)
                    get_tts_mp3.upload_log(message)
                    return None

        if (len(client.voice_clients) > 0) and (not message.content == "!?���?�?"):
            if get_tts_mp3.get_recent_use():
                channel = message.channel
                voice_list = client.voice_clients
                await voice_list[0].disconnect(force=True)
                await channel.send("30�? ?��?�� ?��?��?���? ?��?�� ?��갔습?��?��.", delete_after=120.0)

        if not str(message.author) == "메콩�?#5381":
            pass

        # sender�? bot?�� 경우 ignore
        if message.author.bot:
            return None

        # ?���?
        if message.content == '!?���?' or message.content == "!time" or message.content == "!TIME":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            now = time.localtime()
            string = "%04d?�� %02d?�� %02d?�� %02d?�� %02d�? %02d�?" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            msg = "?��?�� ?��간�? " + string + " ?��?��?��. (GMT+9)"
            await channel.send(msg)
            return None

        if message.content.startswith("!?��?�� "):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            cal = message.content.replace("!?��?�� ", "")
            python_cal = cal.replace("x", "*").replace("X", "*").replace("÷", "/")

            try:
                msg = '"{}"?�� ?��?�� 결과\n{}'.format(cal, eval(python_cal))
            except:
                msg = '"{}"?�� ?��?�� 결과\n{}'.format(cal, "?��바른 ?��?�� ?��?��?���? ?��?�� 계산?�� ?���? ?��?��?��?��?��.")

            await channel.send(msg)
            return None

        # 미니게임 ?��간표
        if message.content == "!미겜":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            msg = Mini.get_recent_minigame()
            await channel.send(msg)
            return None

        # OX ?�즈 �??��?���?
        if message.content == '!ox' or message.content == '!OX' or message.content == '!?�즈' or message.content == '!?��' or message.content == '!q':
            channel = message.channel
            msg = "?��?��?�� ?��?��?���? ?��?��?��?��!!"
            await channel.send(msg)
            return None

        if message.content.startswith('!ox ') or message.content.startswith('!OX ') or message.content.startswith(
                '!?�즈 ') or message.content.startswith('!?�� ') or message.content.startswith('!q '):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            start = time.time()

            try:
                keyword = message.content.replace("!ox ", "", 1).replace("!OX ", "", 1).replace("!?�즈 ", "", 1).replace(
                    "!?�� ", "", 1).replace("!q ", "", 1).lstrip().rstrip()

                if len(keyword) < 2:
                    msg = "�??��?��?�� 2�??�� ?��?�� ?��?��?��주세?��."
                    await channel.send(msg)
                    return None

                msg = inner_query.get_query_result(keyword, message, start)
                await channel.send(msg)
                return None

            except Exception as e:
                Write_error_log.write_log(return_location(), str(e))
                return None

        # ?���? �??��
        if message.content.startswith("!?���?"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            start = time.time()

            if message.content == "!?���?":
                await channel.send("?��?��?���? ?��?��?��주세?��. (ex. !?���? 5)")
                return None

            keyword = re.findall('\d+', message.content)[0]

            try:
                msg = inner_query.get_boss(keyword, message, start)
                await channel.send(msg)
                return None

            except Exception as e:
                Write_error_log.write_log(return_location(), str(e))
                return None

        if message.content.startswith("!길트"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            if message.content == "!길트" or message.content == "!길트 ":
                msg = get_ranking.get_guild_ranking("realtime")
                await channel.send(msg)
                return None

            if message.content == "!길트�?" or message.content == "!길트�? ":
                msg = get_ranking.get_guild_ranking("None") \
                      + "-?�� ?��?��?�� 종합 ?��?���? ?��루에 ?���? ?��?��?��?�� ?��?��?��.-"
                await channel.send(msg)
                return None

            if not message.content.find("!길트�?") == -1:
                keyword = message.content.replace("!길트�? ", "", 1)
                guild_list = get_ranking.get_guild_ranking_search_by_keyword("None", keyword)

                if str(type(guild_list)) == "<class 'str'>":
                    msg = guild_list
                    await channel.send(msg)
                    return None

                guild_list[0]['guildmsg'] += "-?�� ?��?��?�� 종합 ?��?���? ?��루에 ?���? ?��?��?��?�� ?��?��?��.-"

                urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
                await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

                msg = guild_list[0]['guildmsg']
                await channel.send(msg)
                return None

            keyword = message.content.replace("!길트 ", "", 1)
            guild_list = get_ranking.get_guild_ranking_search_by_keyword("realtime", keyword)

            if str(type(guild_list)) == "<class 'str'>":
                msg = guild_list
                await channel.send(msg)
                return None

            urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
            await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

            msg = guild_list[0]['guildmsg']
            await channel.send(msg)
            return None

        if message.content.startswith("!개트"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            if message.content == "!개트" or message.content == "!개트 ":
                msg = get_ranking.get_person_ranking("realtime")
                await channel.send(msg)
                return None

            if message.content == "!개트�?" or message.content == "!개트�? ":
                msg = get_ranking.get_person_ranking("None") \
                      + "\n-?�� ?��?��?�� 종합 ?��?���? ?��루에 ?���? ?��?��?��?�� ?��?��?��.-"
                await channel.send(msg)
                return None

            if not message.content.find("!개트�?") == -1:
                keyword = message.content.replace("!개트�? ", "", 1)
                person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

                if str(type(person_list)) == "<class 'str'>":
                    msg = person_list
                    await channel.send(msg)
                    return None

                person_list[0]['personmsg'] += "-?�� ?��?��?�� 종합 ?��?���? ?��루에 ?���? ?��?��?��?�� ?��?��?��.-"

                urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
                await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

                msg = person_list[0]['personmsg']
                await channel.send(msg)
                return None

            keyword = message.content.replace("!개트 ", "", 1)
            person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

            if str(type(person_list)) == "<class 'str'>":
                msg = person_list
                await channel.send(msg)
                return None

            urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
            await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

            msg = person_list[0]['personmsg']
            await channel.send(msg)
            return None

        if message.content == "!?��?��":
            channel = message.channel
            embed = discord.Embed(title="?��?�� 방법",
                                  description="\"!?��?�� (???��)(?��?��)(볼륨)(반말?���?)\"�? ?��출해주세?��. (?��?��?���? ?��?��!)\n?��?�� �?경도 ?��?��?��?��?��. ?�� 메시�??�� 120�? ?�� ?��?��?��?��?��.")
            embed.add_field(name="???��", value="1: ?��?�� 차분?�� ?��?���?\n2: ?��?�� 차분?�� ?��?���?\n3: ?��?�� 밝�? ???���?\n4: ?��?�� 밝�? ???���?", inline=False)
            embed.add_field(name="?��?��", value="1: ?���?\n2: 보통\n3: 빠름", inline=False)
            embed.add_field(name="볼륨", value="1: 0.7�?\n2: 1.0�?\n3: 1.4�?", inline=False)
            embed.add_field(name="반말 ?���? (\"?��?��?��?��?��\"?���? ?��?��?��?�� \"?��?��\"?��?���? 말함.)", value="1: ?��?�� ?��?��\n2: ?��?��", inline=False)
            embed.add_field(name="?��?�� ?��?��", value="!?��?�� 2221", inline=False)

            await channel.send(embed=embed, delete_after=120.0)
            return None

        if message.content.startswith("!?��?�� "):
            channel = message.channel
            value = message.content.replace("!?��?�� ", "", 1)
            try:
                value_list = [int(value[0]) - 1, int(value[1]) - 1, int(value[2]) - 1, int(value[3]) - 1]

                if not 0 <= int(value_list[0]) <= 3:
                    msg = "?���? ?�� ???�� �? ?��?��?��."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[1]) <= 2:
                    msg = "?���? ?�� ?��?�� �? ?��?��?��."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[2]) <= 2:
                    msg = "?���? ?�� 볼륨 �? ?��?��?��."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[3]) <= 1:
                    msg = "?���? ?�� 반말 ?���? �? ?��?��?��."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if get_tts_mp3.upload_user_setting(message, value_list):
                    msg = "?��?�� ?���?!"
                    await channel.send(msg)
                    return None

                else:
                    msg = "?���? 문제�? ?��?�� ?��?��?���? 못했?��?��?��."
                    await channel.send(msg)
                    return None

            except:
                msg = "?���? ?�� 값을 ?��?��?��?��?��?��?��."
                await channel.send(msg)
                return None

        if message.content == "!?��?��?��?��":
            channel = message.channel
            now_setting = get_tts_mp3.configure_setting_text(message)

            if len(now_setting) == 0:
                await channel.send('?��?�� 값이 ?��?��?��?��.')
                return None

            embed = discord.Embed(title="?��?�� ?��?�� (카카?�� API)")
            embed.add_field(name="???��", value=str(now_setting[0]), inline=False)
            embed.add_field(name="?��?��", value=str(now_setting[1]), inline=False)
            embed.add_field(name="볼륨", value=str(now_setting[2]), inline=False)
            embed.add_field(name="반말 ?���? (\"?��?��?��?��?��\"?���? ?��?��?��?�� \"?��?��\"?��?���? 말함.)", value=str(now_setting[3]), inline=False)
            await channel.send("<@" + str(message.author.id) + "> ?��?�� ?��?�� ?��?��?��?��?��.", embed=embed, delete_after=120.0)

        if message.content == "!?���?�?":
            channel = message.channel
            voice_list = client.voice_clients

            if len(voice_list) == 0:
                await channel.send('?��?���? 보이?�� 채널?�� ?��?��?��?��.', delete_after=10.0)
                return None
            else:
                await voice_list[0].disconnect(force=True)
                await channel.send('?���?�? ?���?', delete_after=10.0)
                return None

        if message.content.startswith("!"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            msg = inner_query.get_custom_query(message)

            if not msg == "False":
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
    if Backup_Task.backup_db():
        Write_error_log.write_log(return_location(), "Backup Task Finished")
    else:
        Write_error_log.write_log(return_location(), "Backup Task Failed")


if __name__ == "__main__":
    client = chatbot()
    thread_1 = threading.Thread(target=thread_execute)
    thread_1.start()

    Write_error_log.write_log(return_location(), "Thread Start")
    # BOT Token
    # Main Token = "{DISCORD_BOT_TOKEN}"
    token = "{DISCORD_BOT_TOKEN}"

    # Dev Token = "{DISCORD_BOT_TOKEN}"
    # token = "{DISCORD_BOT_TOKEN}"
    client.run(token)

