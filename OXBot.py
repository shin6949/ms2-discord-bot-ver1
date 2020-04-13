import re
import time
import urllib.request
import schedule
import discord
from pprint import pprint
import threading

# λ³λ ??Ό
import Mini
import get_ranking
import get_tts_mp3
import inner_query
import Backup_Task
import Write_error_log


# λ©μ½©OXλ΄?#5381

def return_location():
    return "GuildOXBot - OXBot.py"


def where_user_in(message):
    user_id = message.author.id
    guild_voice_list = message.guild.voice_channels

    for i in guild_voice_list:
        for j in range(len(i.members)):
            # i μ±λ? ? ??κ°? ??Όλ©?
            if str(i.members[j].id) == str(user_id):
                # ? ??κ°? ?? λ³΄μ΄?€ μ±λ? λ¦¬ν΄
                return i

    return "False"


def judge_server(message):
    try:
        if not str(message.guild.id) == "{DISCORD_SERVER_ID}" and not str(message.guild.id) == "{DISCORD_SERVER_ID}":
            msg = "?΄ λ΄μ? μ§?? ? ?λ²μ?λ§? ?¬?©??€ ? ??΅??€."
            return msg
        else:
            return "True"

    except:
        msg = "?΄ λ΄μ? DM λͺ¨λλ‘λ ?¬?©??€ ? ??΅??€."
        return msg


class chatbot(discord.Client):
    async def on_ready(self):
        game = discord.Game("!?€λͺμ, !??Όλ‘? λ¬Έμ  κ²??")
        await client.change_presence(status=discord.Status.online, activity=game)
        print("READY")

    async def on_message(self, message):
        if message.content.startswith("\"\" "):
            channel = message.channel
            voice_channel = where_user_in(message)

            if voice_channel == "False":
                await channel.send('?€?΄κ°? ?? λ³΄μ΄?€ μ±λ?΄ ??΅??€.', delete_after=10.0)
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
                        msg = "λ¨Όμ? ?μ²?? λ©μμ§?λ₯? ?¬??κ³? ??΅??€."
                        await channel.send(msg, delete_after=10.0)
                        get_tts_mp3.upload_log(message)
                        return None
                else:
                    msg = "?λ²? λ¬Έμ λ‘? ?Έ?΄ TTS κ΅¬μ±? ?€?¨????΅??€."
                    await channel.send(msg, delete_after=10.0)
                    get_tts_mp3.upload_log(message)
                    return None

        if (len(client.voice_clients) > 0) and (not message.content == "!?κ°?κΈ?"):
            if get_tts_mp3.get_recent_use():
                channel = message.channel
                voice_list = client.voice_clients
                await voice_list[0].disconnect(force=True)
                await channel.send("30λΆ? ?΄? ?¬?©?μ§? ?? ?κ°μ΅??€.", delete_after=120.0)

        if not str(message.author) == "λ©μ½©λ΄?#5381":
            pass

        # senderκ°? bot?Ό κ²½μ° ignore
        if message.author.bot:
            return None

        # ?κ°?
        if message.content == '!?κ°?' or message.content == "!time" or message.content == "!TIME":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            now = time.localtime()
            string = "%04d? %02d? %02d?Ό %02d? %02dλΆ? %02dμ΄?" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            msg = "??¬ ?κ°μ? " + string + " ???€. (GMT+9)"
            await channel.send(msg)
            return None

        if message.content.startswith("!?°?° "):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            cal = message.content.replace("!?°?° ", "")
            python_cal = cal.replace("x", "*").replace("X", "*").replace("Γ·", "/")

            try:
                msg = '"{}"? ?°?° κ²°κ³Ό\n{}'.format(cal, eval(python_cal))
            except:
                msg = '"{}"? ?°?° κ²°κ³Ό\n{}'.format(cal, "?¬λ°λ₯Έ ?? ?? ₯?μ§? ?? κ³μ°?΄ ?μ§? ???΅??€.")

            await channel.send(msg)
            return None

        # λ―Έλκ²μ ?κ°ν
        if message.content == "!λ―Έκ²":
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            msg = Mini.get_recent_minigame()
            await channel.send(msg)
            return None

        # OX ?΄μ¦ κ²???κΈ?
        if message.content == '!ox' or message.content == '!OX' or message.content == '!?΄μ¦' or message.content == '!?' or message.content == '!q':
            channel = message.channel
            msg = "?? ₯? ?€??κ°? ??΅??€!!"
            await channel.send(msg)
            return None

        if message.content.startswith('!ox ') or message.content.startswith('!OX ') or message.content.startswith(
                '!?΄μ¦ ') or message.content.startswith('!? ') or message.content.startswith('!q '):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            start = time.time()

            try:
                keyword = message.content.replace("!ox ", "", 1).replace("!OX ", "", 1).replace("!?΄μ¦ ", "", 1).replace(
                    "!? ", "", 1).replace("!q ", "", 1).lstrip().rstrip()

                if len(keyword) < 2:
                    msg = "κ²???΄? 2κΈ?? ?΄? ?? ₯?΄μ£ΌμΈ?."
                    await channel.send(msg)
                    return None

                msg = inner_query.get_query_result(keyword, message, start)
                await channel.send(msg)
                return None

            except Exception as e:
                Write_error_log.write_log(return_location(), str(e))
                return None

        # ?λ³? κ²??
        if message.content.startswith("!?λ³?"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            start = time.time()

            if message.content == "!?λ³?":
                await channel.send("?€??λ₯? ?? ₯?΄μ£ΌμΈ?. (ex. !?λ³? 5)")
                return None

            keyword = re.findall('\d+', message.content)[0]

            try:
                msg = inner_query.get_boss(keyword, message, start)
                await channel.send(msg)
                return None

            except Exception as e:
                Write_error_log.write_log(return_location(), str(e))
                return None

        if message.content.startswith("!κΈΈνΈ"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            if message.content == "!κΈΈνΈ" or message.content == "!κΈΈνΈ ":
                msg = get_ranking.get_guild_ranking("realtime")
                await channel.send(msg)
                return None

            if message.content == "!κΈΈνΈμ’?" or message.content == "!κΈΈνΈμ’? ":
                msg = get_ranking.get_guild_ranking("None") \
                      + "-?΄ ??? μ’ν© ??λ‘? ?λ£¨μ ?λ²? ??°?΄?Έ ?©??€.-"
                await channel.send(msg)
                return None

            if not message.content.find("!κΈΈνΈμ’?") == -1:
                keyword = message.content.replace("!κΈΈνΈμ’? ", "", 1)
                guild_list = get_ranking.get_guild_ranking_search_by_keyword("None", keyword)

                if str(type(guild_list)) == "<class 'str'>":
                    msg = guild_list
                    await channel.send(msg)
                    return None

                guild_list[0]['guildmsg'] += "-?΄ ??? μ’ν© ??λ‘? ?λ£¨μ ?λ²? ??°?΄?Έ ?©??€.-"

                urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
                await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

                msg = guild_list[0]['guildmsg']
                await channel.send(msg)
                return None

            keyword = message.content.replace("!κΈΈνΈ ", "", 1)
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

        if message.content.startswith("!κ°νΈ"):
            channel = message.channel

            judge = judge_server(message)
            if not judge == "True":
                await channel.send(judge)
                return None

            if message.content == "!κ°νΈ" or message.content == "!κ°νΈ ":
                msg = get_ranking.get_person_ranking("realtime")
                await channel.send(msg)
                return None

            if message.content == "!κ°νΈμ’?" or message.content == "!κ°νΈμ’? ":
                msg = get_ranking.get_person_ranking("None") \
                      + "\n-?΄ ??? μ’ν© ??λ‘? ?λ£¨μ ?λ²? ??°?΄?Έ ?©??€.-"
                await channel.send(msg)
                return None

            if not message.content.find("!κ°νΈμ’?") == -1:
                keyword = message.content.replace("!κ°νΈμ’? ", "", 1)
                person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

                if str(type(person_list)) == "<class 'str'>":
                    msg = person_list
                    await channel.send(msg)
                    return None

                person_list[0]['personmsg'] += "-?΄ ??? μ’ν© ??λ‘? ?λ£¨μ ?λ²? ??°?΄?Έ ?©??€.-"

                urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
                await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

                msg = person_list[0]['personmsg']
                await channel.send(msg)
                return None

            keyword = message.content.replace("!κ°νΈ ", "", 1)
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

        if message.content == "!?€? ":
            channel = message.channel
            embed = discord.Embed(title="?€?  λ°©λ²",
                                  description="\"!?€?  (???)(??)(λ³Όλ₯¨)(λ°λ§?¬λΆ?)\"λ‘? ? μΆν΄μ£ΌμΈ?. (??΄?°κΈ? ??΄!)\n?€?  λ³?κ²½λ ??Ό?©??€. ?΄ λ©μμ§?? 120μ΄? ? ?­? ?©??€.")
            embed.add_field(name="???", value="1: ?¬?± μ°¨λΆ? ?­?μ²?\n2: ?¨?± μ°¨λΆ? ?­?μ²?\n3: ?¬?± λ°μ? ???μ²?\n4: ?¨?± λ°μ? ???μ²?", inline=False)
            embed.add_field(name="??", value="1: ?λ¦?\n2: λ³΄ν΅\n3: λΉ λ¦", inline=False)
            embed.add_field(name="λ³Όλ₯¨", value="1: 0.7λ°?\n2: 1.0λ°?\n3: 1.4λ°?", inline=False)
            embed.add_field(name="λ°λ§ ?¬λΆ? (\"????Έ?\"?Όκ³? ?? ₯?΄? \"??\"?΄?Όκ³? λ§ν¨.)", value="1: ?€?  ??¨\n2: ?€? ", inline=False)
            embed.add_field(name="?€?  ??", value="!?€?  2221", inline=False)

            await channel.send(embed=embed, delete_after=120.0)
            return None

        if message.content.startswith("!?€?  "):
            channel = message.channel
            value = message.content.replace("!?€?  ", "", 1)
            try:
                value_list = [int(value[0]) - 1, int(value[1]) - 1, int(value[2]) - 1, int(value[3]) - 1]

                if not 0 <= int(value_list[0]) <= 3:
                    msg = "?λͺ? ? ??? κ°? ???€."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[1]) <= 2:
                    msg = "?λͺ? ? ?? κ°? ???€."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[2]) <= 2:
                    msg = "?λͺ? ? λ³Όλ₯¨ κ°? ???€."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if not 0 <= int(value_list[3]) <= 1:
                    msg = "?λͺ? ? λ°λ§ ?¬λΆ? κ°? ???€."
                    await channel.send(msg, delete_after=10.0)
                    return None

                if get_tts_mp3.upload_user_setting(message, value_list):
                    msg = "?€?  ?λ£?!"
                    await channel.send(msg)
                    return None

                else:
                    msg = "?λ²? λ¬Έμ λ‘? ?Έ?΄ ?€? ?μ§? λͺ»ν?΅??€."
                    await channel.send(msg)
                    return None

            except:
                msg = "?λͺ? ? κ°μ ?? ₯??¨?΅??€."
                await channel.send(msg)
                return None

        if message.content == "!??¬?€? ":
            channel = message.channel
            now_setting = get_tts_mp3.configure_setting_text(message)

            if len(now_setting) == 0:
                await channel.send('?€?  κ°μ΄ ??΅??€.')
                return None

            embed = discord.Embed(title="??¬ ?€?  (μΉ΄μΉ΄?€ API)")
            embed.add_field(name="???", value=str(now_setting[0]), inline=False)
            embed.add_field(name="??", value=str(now_setting[1]), inline=False)
            embed.add_field(name="λ³Όλ₯¨", value=str(now_setting[2]), inline=False)
            embed.add_field(name="λ°λ§ ?¬λΆ? (\"????Έ?\"?Όκ³? ?? ₯?΄? \"??\"?΄?Όκ³? λ§ν¨.)", value=str(now_setting[3]), inline=False)
            await channel.send("<@" + str(message.author.id) + "> ?? ??¬ ?€? ???€.", embed=embed, delete_after=120.0)

        if message.content == "!?κ°?κΈ?":
            channel = message.channel
            voice_list = client.voice_clients

            if len(voice_list) == 0:
                await channel.send('?€?΄κ°? λ³΄μ΄?€ μ±λ?΄ ??΅??€.', delete_after=10.0)
                return None
            else:
                await voice_list[0].disconnect(force=True)
                await channel.send('?κ°?κΈ? ?λ£?', delete_after=10.0)
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

