import re
import time
import urllib.request
import schedule
import discord
from pprint import pprint
import threading

# ë³„ë„ ?ŒŒ?¼
import Mini
import get_ranking
import get_tts_mp3
import inner_query
import Backup_Task
import Write_error_log


# ë©”ì½©OXë´?#5381

def return_location():
    return "GuildOXBot - OXBot.py"


def where_user_in(message):
    user_id = message.author.id
    guild_voice_list = message.guild.voice_channels

    for i in guild_voice_list:
        for j in range(len(i.members)):
            # i ì±„ë„?— ?œ ??ê°? ?ˆ?œ¼ë©?
            if str(i.members[j].id) == str(user_id):
                # ?œ ??ê°? ?ˆ?Š” ë³´ì´?Š¤ ì±„ë„?„ ë¦¬í„´
                return i

    return "False"


def judge_server(message):
    try:
        if not str(message.guild.id) == "{DISCORD_SERVER_ID}" and not str(message.guild.id) == "{DISCORD_SERVER_ID}":
            msg = "?´ ë´‡ì? ì§?? •?œ ?„œë²„ì—?„œë§? ?‚¬?š©?•˜?‹¤ ?ˆ˜ ?ˆ?Šµ?‹ˆ?‹¤."
            return msg
        else:
            return "True"

    except:
        msg = "?´ ë´‡ì? DM ëª¨ë“œë¡œëŠ” ?‚¬?š©?•˜?‹¤ ?ˆ˜ ?—†?Šµ?‹ˆ?‹¤."
        return msg


class chatbot(discord.Client):
    async def on_ready(self):
        game = discord.Game("!?„¤ëª…ì„œ, !?…‹?œ¼ë¡? ë¬¸ì œ ê²??ƒ‰")
        await client.change_presence(status=discord.Status.online, activity=game)
        print("READY")

    async def on_message(self, message):
        if message.content.startswith("\"\" "):
            channel = message.channel
            voice_channel = where_user_in(message)

            if voice_channel == "False":
                await channel.send('?“¤?–´ê°? ?ˆ?Š” ë³´ì´?Š¤ ì±„ë„?´ ?—†?Šµ?‹ˆ?‹¤.', delete_after=10.0)
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
                        msg = "ë¨¼ì? ?š”ì²??•œ ë©”ì‹œì§?ë¥? ?¬?ƒ?•˜ê³? ?ˆ?Šµ?‹ˆ?‹¤."
                        await channel.send(msg, delete_after=10.0)
                        get_tts_mp3.upload_log(message)
                        return None
                else:
                    msg = "?„œë²? ë¬¸ì œë¡? ?¸?•´ TTS êµ¬ì„±?— ?‹¤?Œ¨?•˜???Šµ?‹ˆ?‹¤."
                    await channel.send(msg, delete_after=10.0)
                    get_tts_mp3.upload_log(message)
                    return None

        if (len(client.voice_clients) > 0) and (not message.content == "!?‚˜ê°?ê¸?"):
            if get_tts_mp3.get_recent_use():
                channel = message.channel
                voice_list = client.voice_clients
                await voice_list[0].disconnect(force=True)
                await channel.send("30ë¶? ?´?ƒ ?‚¬?š©?•˜ì§? ?•Š?•„ ?‚˜ê°”ìŠµ?‹ˆ?‹¤.", delete_after=120.0)

        if not str(message.author) == "ë©”ì½©ë´?#5381":
            pass

        # senderê°? bot?¼ ê²½ìš° ignore
        if message.author.bot:
            return None

        # ?‹œê°?
        if message.content == '!?‹œê°?' or message.content == "!time" or message.content == "!TIME":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            now = time.localtime()
            string = "%04d?…„ %02d?›” %02d?¼ %02d?‹œ %02dë¶? %02dì´?" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            msg = "?˜„?¬ ?‹œê°„ì? " + string + " ?…?‹ˆ?‹¤. (GMT+9)"
            await channel.send(msg)
            return None

        if message.content.startswith("!?—°?‚° "):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            cal = message.content.replace("!?—°?‚° ", "")
            python_cal = cal.replace("x", "*").replace("X", "*").replace("Ã·", "/")

            try:
                msg = '"{}"?˜ ?—°?‚° ê²°ê³¼\n{}'.format(cal, eval(python_cal))
            except:
                msg = '"{}"?˜ ?—°?‚° ê²°ê³¼\n{}'.format(cal, "?˜¬ë°”ë¥¸ ?‹?„ ?…? ¥?•˜ì§? ?•Š?•„ ê³„ì‚°?´ ?˜ì§? ?•Š?•˜?Šµ?‹ˆ?‹¤.")

            await channel.send(msg)
            return None

        # ë¯¸ë‹ˆê²Œì„ ?‹œê°„í‘œ
        if message.content == "!ë¯¸ê²œ":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            msg = Mini.get_recent_minigame()
            await channel.send(msg)
            return None

        # OX ?´ì¦ˆ ê²??ƒ‰?•˜ê¸?
        if message.content == '!ox' or message.content == '!OX' or message.content == '!?´ì¦ˆ' or message.content == '!?…‹' or message.content == '!q':
            channel = message.channel
            msg = "?…? ¥?•œ ?‚¤?›Œ?“œê°? ?—†?Šµ?‹ˆ?‹¤!!"
            await channel.send(msg)
            return None

        if message.content.startswith('!ox ') or message.content.startswith('!OX ') or message.content.startswith(
                '!?´ì¦ˆ ') or message.content.startswith('!?…‹ ') or message.content.startswith('!q '):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            start = time.time()

            try:
                keyword = message.content.replace("!ox ", "", 1).replace("!OX ", "", 1).replace("!?´ì¦ˆ ", "", 1).replace(
                    "!?…‹ ", "", 1).replace("!q ", "", 1).lstrip().rstrip()

                if len(keyword) < 2:
                    msg = "ê²??ƒ‰?–´?Š” 2ê¸?? ?´?ƒ ?…? ¥?•´ì£¼ì„¸?š”."
                    await channel.send(msg)
                    return None

                msg = inner_query.get_query_result(keyword, message, start)
                await channel.send(msg)
                return None

            except Exception as e:
                Write_error_log.write_log(return_location(), str(e))
                return None

        # ?•„ë³? ê²??ƒ‰
        if message.content.startswith("!?•„ë³?"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            start = time.time()

            if message.content == "!?•„ë³?":
                await channel.send("?‚¤?›Œ?“œë¥? ?…? ¥?•´ì£¼ì„¸?š”. (ex. !?•„ë³? 5)")
                return None

            keyword = re.findall('\d+', message.content)[0]

            try:
                msg = inner_query.get_boss(keyword, message, start)
                await channel.send(msg)
                return None

            except Exception as e:
                Write_error_log.write_log(return_location(), str(e))
                return None

        if message.content.startswith("!ê¸¸íŠ¸"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            if message.content == "!ê¸¸íŠ¸" or message.content == "!ê¸¸íŠ¸ ":
                msg = get_ranking.get_guild_ranking("realtime")
                await channel.send(msg)
                return None

            if message.content == "!ê¸¸íŠ¸ì¢?" or message.content == "!ê¸¸íŠ¸ì¢? ":
                msg = get_ranking.get_guild_ranking("None") \
                      + "-?´ ?ˆœ?œ„?Š” ì¢…í•© ?ˆœ?œ„ë¡? ?•˜ë£¨ì— ?•œë²? ?—…?°?´?Š¸ ?©?‹ˆ?‹¤.-"
                await channel.send(msg)
                return None

            if not message.content.find("!ê¸¸íŠ¸ì¢?") == -1:
                keyword = message.content.replace("!ê¸¸íŠ¸ì¢? ", "", 1)
                guild_list = get_ranking.get_guild_ranking_search_by_keyword("None", keyword)

                if str(type(guild_list)) == "<class 'str'>":
                    msg = guild_list
                    await channel.send(msg)
                    return None

                guild_list[0]['guildmsg'] += "-?´ ?ˆœ?œ„?Š” ì¢…í•© ?ˆœ?œ„ë¡? ?•˜ë£¨ì— ?•œë²? ?—…?°?´?Š¸ ?©?‹ˆ?‹¤.-"

                urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
                await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

                msg = guild_list[0]['guildmsg']
                await channel.send(msg)
                return None

            keyword = message.content.replace("!ê¸¸íŠ¸ ", "", 1)
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

        if message.content.startswith("!ê°œíŠ¸"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            if message.content == "!ê°œíŠ¸" or message.content == "!ê°œíŠ¸ ":
                msg = get_ranking.get_person_ranking("realtime")
                await channel.send(msg)
                return None

            if message.content == "!ê°œíŠ¸ì¢?" or message.content == "!ê°œíŠ¸ì¢? ":
                msg = get_ranking.get_person_ranking("None") \
                      + "\n-?´ ?ˆœ?œ„?Š” ì¢…í•© ?ˆœ?œ„ë¡? ?•˜ë£¨ì— ?•œë²? ?—…?°?´?Š¸ ?©?‹ˆ?‹¤.-"
                await channel.send(msg)
                return None

            if not message.content.find("!ê°œíŠ¸ì¢?") == -1:
                keyword = message.content.replace("!ê°œíŠ¸ì¢? ", "", 1)
                person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

                if str(type(person_list)) == "<class 'str'>":
                    msg = person_list
                    await channel.send(msg)
                    return None

                person_list[0]['personmsg'] += "-?´ ?ˆœ?œ„?Š” ì¢…í•© ?ˆœ?œ„ë¡? ?•˜ë£¨ì— ?•œë²? ?—…?°?´?Š¸ ?©?‹ˆ?‹¤.-"

                urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
                await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

                msg = person_list[0]['personmsg']
                await channel.send(msg)
                return None

            keyword = message.content.replace("!ê°œíŠ¸ ", "", 1)
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

        if message.content == "!?„¤? •":
            channel = message.channel
            embed = discord.Embed(title="?„¤? • ë°©ë²•",
                                  description="\"!?„¤? • (???…)(?†?„)(ë³¼ë¥¨)(ë°˜ë§?—¬ë¶?)\"ë¡? ? œì¶œí•´ì£¼ì„¸?š”. (?„?–´?“°ê¸? ?—†?´!)\n?„¤? • ë³?ê²½ë„ ?™?¼?•©?‹ˆ?‹¤. ?´ ë©”ì‹œì§??Š” 120ì´? ?›„ ?‚­? œ?©?‹ˆ?‹¤.")
            embed.add_field(name="???…", value="1: ?—¬?„± ì°¨ë¶„?•œ ?‚­?…ì²?\n2: ?‚¨?„± ì°¨ë¶„?•œ ?‚­?…ì²?\n3: ?—¬?„± ë°ì? ???™”ì²?\n4: ?‚¨?„± ë°ì? ???™”ì²?", inline=False)
            embed.add_field(name="?†?„", value="1: ?Šë¦?\n2: ë³´í†µ\n3: ë¹ ë¦„", inline=False)
            embed.add_field(name="ë³¼ë¥¨", value="1: 0.7ë°?\n2: 1.0ë°?\n3: 1.4ë°?", inline=False)
            embed.add_field(name="ë°˜ë§ ?—¬ë¶? (\"?•ˆ?…•?•˜?„¸?š”\"?¼ê³? ?…? ¥?•´?„ \"?•ˆ?…•\"?´?¼ê³? ë§í•¨.)", value="1: ?„¤? • ?•ˆ?•¨\n2: ?„¤? •", inline=False)
            embed.add_field(name="?„¤? • ?˜ˆ?‹œ", value="!?„¤? • 2221", inline=False)

            await channel.send(embed=embed, delete_after=120.0)
            return None

        if message.content.startswith("!?„¤? • "):
            channel = message.channel
            value = message.content.replace("!?„¤? • ", "", 1)
            try:
                value_list = [int(value[0]) - 1, int(value[1]) - 1, int(value[2]) - 1, int(value[3]) - 1]

                if not 0 <= int(value_list[0]) <= 3:
                    msg = "?˜ëª? ?œ ???… ê°? ?…?‹ˆ?‹¤."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[1]) <= 2:
                    msg = "?˜ëª? ?œ ?†?„ ê°? ?…?‹ˆ?‹¤."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[2]) <= 2:
                    msg = "?˜ëª? ?œ ë³¼ë¥¨ ê°? ?…?‹ˆ?‹¤."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[3]) <= 1:
                    msg = "?˜ëª? ?œ ë°˜ë§ ?—¬ë¶? ê°? ?…?‹ˆ?‹¤."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if get_tts_mp3.upload_user_setting(message, value_list):
                    msg = "?„¤? • ?™„ë£?!"
                    await channel.send(msg)
                    return None

                else:
                    msg = "?„œë²? ë¬¸ì œë¡? ?¸?•´ ?„¤? •?•˜ì§? ëª»í–ˆ?Šµ?‹ˆ?‹¤."
                    await channel.send(msg)
                    return None

            except:
                msg = "?˜ëª? ?œ ê°’ì„ ?…? ¥?•˜?…¨?Šµ?‹ˆ?‹¤."
                await channel.send(msg)
                return None

        if message.content == "!?˜„?¬?„¤? •":
            channel = message.channel
            now_setting = get_tts_mp3.configure_setting_text(message)

            if len(now_setting) == 0:
                await channel.send('?„¤? • ê°’ì´ ?—†?Šµ?‹ˆ?‹¤.')
                return None

            embed = discord.Embed(title="?˜„?¬ ?„¤? • (ì¹´ì¹´?˜¤ API)")
            embed.add_field(name="???…", value=str(now_setting[0]), inline=False)
            embed.add_field(name="?†?„", value=str(now_setting[1]), inline=False)
            embed.add_field(name="ë³¼ë¥¨", value=str(now_setting[2]), inline=False)
            embed.add_field(name="ë°˜ë§ ?—¬ë¶? (\"?•ˆ?…•?•˜?„¸?š”\"?¼ê³? ?…? ¥?•´?„ \"?•ˆ?…•\"?´?¼ê³? ë§í•¨.)", value=str(now_setting[3]), inline=False)
            await channel.send("<@" + str(message.author.id) + "> ?‹˜?˜ ?˜„?¬ ?„¤? •?…?‹ˆ?‹¤.", embed=embed, delete_after=120.0)

        if message.content == "!?‚˜ê°?ê¸?":
            channel = message.channel
            voice_list = client.voice_clients

            if len(voice_list) == 0:
                await channel.send('?“¤?–´ê°? ë³´ì´?Š¤ ì±„ë„?´ ?—†?Šµ?‹ˆ?‹¤.', delete_after=10.0)
                return None
            else:
                await voice_list[0].disconnect(force=True)
                await channel.send('?‚˜ê°?ê¸? ?™„ë£?', delete_after=10.0)
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

