import random
import re
import time
import urllib.request

import discord

# 별도 파일
import Mini
import get_ranking
import get_tts_mp3
import inner_query

# 메콩OX봇#5381


def where_user_in(message):
    user_id = message.author.id
    guild_voice_list = message.guild.voice_channels

    for i in guild_voice_list:
        for j in range(len(i.members)):
            # i 채널에 유저가 있으면
            if str(i.members[j].id) == str(user_id):
                # 유저가 있는 보이스 채널을 리턴
                return i

    return "False"


def judge_server(message, channel):
    try:
        if not str(message.guild.id) == "{DISCORD_SERVER_ID}" and not str(message.guild.id) == "{DISCORD_SERVER_ID}":
            msg = "이 봇은 지정된 서버에서만 사용하실 수 있습니다."
            return msg
        else:
            return "True"

    except:
        msg = "이 봇은 DM 모드로는 사용하실 수 없습니다."
        return msg


client = discord.Client()

# BOT Token
# Main Token = "{DISCORD_BOT_TOKEN}"
token = "{DISCORD_BOT_TOKEN}"

# Dev Token = "{DISCORD_BOT_TOKEN}"
# token = "{DISCORD_BOT_TOKEN}"


# Bot initialize
@client.event
async def on_ready():
    game = discord.Game("!설명서, !ㅋ으로 문제 검색")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("READY")


# message respond
@client.event
async def on_message(message):
    if message.content.startswith("\"\" "):
        channel = message.channel
        voice_channel = where_user_in(message)

        if voice_channel == "False":
            await channel.send('들어가 있는 보이스 채널이 없습니다.', delete_after=10.0)
            get_tts_mp3.upload_log(message)
            return None
        else:
            keyword = message.content.replace("\"\" ", "", 1)

            if get_tts_mp3.get_kakao_mp3(message, keyword):
                try:
                    current_voiceclient = await voice_channel.connect(timeout=3.0)
                    time.sleep(1)
                except Exception as d:
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
                    msg = "먼저 요청한 메시지를 재생하고 있습니다."
                    await channel.send(msg, delete_after=10.0)
                    get_tts_mp3.upload_log(message)
                    return None
            else:
                msg = "서버 문제로 인해 TTS 구성에 실패하였습니다."
                await channel.send(msg, delete_after=10.0)
                get_tts_mp3.upload_log(message)
                return None

    if (len(client.voice_clients) > 0) and (not message.content == "!나가기"):
        if get_tts_mp3.get_recent_use():
            channel = message.channel
            voice_list = client.voice_clients
            await voice_list[0].disconnect(force=True)
            await channel.send("30분 이상 사용하지 않아 나갔습니다.", delete_after=120.0)

    if not str(message.author) == "메콩봇#5381":
        pass

    # sender가 bot일 경우 ignore
    if message.author.bot:
        return None

    # 시간
    if message.content == '!시간' or message.content == "!time" or message.content == "!TIME":
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        now = time.localtime()
        string = "%04d년 %02d월 %02d일 %02d시 %02d분 %02d초" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        msg = "현재 시간은 " + string + " 입니다. (GMT+9)"
        await channel.send(msg)
        inner_query.log_upload("Other", message.content, message.author)
        return None

    # 주사위 기능 (1~100)
    if message.content == "!주사위" or message.content == "!roll":
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        dice_value = str(random.randrange(0, 100))
        msg = "[" + dice_value + "] 이(가) 나왔습니다!"
        await channel.send(msg)
        inner_query.log_upload("DiceLog", dice_value, message.author)
        return None

    # 미니게임 시간표
    if message.content == "!미겜":
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        msg = Mini.get_recent_minigame()
        await channel.send(msg)
        inner_query.log_upload("Other", message.content, message.author)
        return None

    # OX 퀴즈 검색하기
    if message.content == '!ox' or message.content == '!OX' or message.content == '!퀴즈' or message.content == '!ㅋ' or message.content == '!q':
        channel = message.channel
        msg = "입력한 키워드가 없습니다!!"
        await channel.send(msg)
        inner_query.log_upload("QueryLog", message.content, message.author)
        return None

    if message.content.startswith('!ox ') or message.content.startswith('!OX ') or message.content.startswith('!퀴즈 ') or message.content.startswith('!ㅋ ') or message.content.startswith('!q '):
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        start = time.time()

        try:
            keyword = message.content.replace("!ox ", "", 1).replace("!OX ", "", 1).replace("!퀴즈 ", "", 1).replace("!ㅋ ", "", 1).replace("!q ", "", 1).lstrip().rstrip()

            if len(keyword) < 2:
                msg = "검색어는 2글자 이상 입력해주세요."
                await channel.send(msg)
                inner_query.log_upload("QueryLog", message.content, message.author)
                return None

            msg = inner_query.get_query_result(keyword, message, start)
            await channel.send(msg)
            inner_query.log_upload("QueryLog", message.content, message.author)
            return None

        except Exception as e:
            print(e)
            return None

    # 필보 검색
    if message.content.startswith("!필보"):
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        start = time.time()

        if message.content == "!필보":
            await channel.send("키워드를 입력해주세요. (ex. !필보 5)")
            return None

        keyword = re.findall('\d+', message.content)[0]

        try:
            msg = inner_query.get_boss(keyword, message, start)
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None

        except Exception as e:
            print(e)
            return None

    if message.content.startswith("!길트"):
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        if message.content == "!길트" or message.content == "!길트 ":
            msg = get_ranking.get_guild_ranking("realtime")
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None

        if message.content == "!길트종" or message.content == "!길트종 ":
            msg = get_ranking.get_guild_ranking("None")\
                  + "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None

        if not message.content.find("!길트종") == -1:
            keyword = message.content.replace("!길트종 ", "", 1)
            guild_list = get_ranking.get_guild_ranking_search_by_keyword("None", keyword)

            if str(type(guild_list)) == "<class 'str'>":
                msg = guild_list
                await channel.send(msg)
                inner_query.log_upload("Other", message.content, message.author)
                return None

            guild_list[0]['guildmsg'] += "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"

            urllib.request.urlretrieve(guild_list[0]['imgurl'], guild_list[0]['name'] + ".png")
            await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

            msg = guild_list[0]['guildmsg']
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None

        keyword = message.content.replace("!길트 ", "", 1)
        guild_list = get_ranking.get_guild_ranking_search_by_keyword("realtime", keyword)

        if str(type(guild_list)) == "<class 'str'>":
            msg = guild_list
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None

        urllib.request.urlretrieve(guild_list[0]['imgurl'],  guild_list[0]['name'] + ".png")
        await channel.send(file=discord.File(guild_list[0]['name'] + ".png"))

        msg = guild_list[0]['guildmsg']
        await channel.send(msg)
        inner_query.log_upload("Other", message.content, message.author)
        return None

    if message.content.startswith("!개트"):
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        if message.content == "!개트" or message.content == "!개트 ":
            msg = get_ranking.get_person_ranking("realtime")
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None
        
        if message.content == "!개트종" or message.content == "!개트종 ":
            msg = get_ranking.get_person_ranking("None")\
                  + "\n-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None
        
        if not message.content.find("!개트종") == -1:
            keyword = message.content.replace("!개트종 ", "", 1)
            person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

            if str(type(person_list)) == "<class 'str'>":
                msg = person_list
                await channel.send(msg)
                inner_query.log_upload("Other", message.content, message.author)
                return None

            person_list[0]['personmsg'] += "-이 순위는 종합 순위로 하루에 한번 업데이트 됩니다.-"

            urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
            await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

            msg = person_list[0]['personmsg']
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None
        
        keyword = message.content.replace("!개트 ", "", 1)
        person_list = get_ranking.get_person_ranking_search_by_keyword("realtime", keyword)

        if str(type(person_list)) == "<class 'str'>":
            msg = person_list
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None

        urllib.request.urlretrieve(person_list[0]['imgurl'], person_list[0]['name'] + ".png")
        await channel.send(file=discord.File(person_list[0]['name'] + ".png"))

        msg = person_list[0]['personmsg']
        await channel.send(msg)
        inner_query.log_upload("Other", message.content, message.author)
        return None

    if message.content == "!설정":
        channel = message.channel
        embed = discord.Embed(title="설정 방법",
                              description="\"!설정 (타입)(속도)(볼륨)(반말여부)\"로 제출해주세요. (띄어쓰기 없이!)\n설정 변경도 동일합니다. 이 메시지는 120초 후 삭제됩니다.")
        embed.add_field(name="타입", value="1: 여성 차분한 낭독체\n2: 남성 차분한 낭독체\n3: 여성 밝은 대화체\n4: 남성 밝은 대화체", inline=False)
        embed.add_field(name="속도", value="1: 느림\n2: 보통\n3: 빠름", inline=False)
        embed.add_field(name="볼륨", value="1: 0.7배\n2: 1.0배\n3: 1.4배", inline=False)
        embed.add_field(name="반말 여부 (\"안녕하세요\"라고 입력해도 \"안녕\"이라고 말함.)", value="1: 설정 안함\n2: 설정", inline=False)
        embed.add_field(name="설정 예시", value="!설정 2221", inline=False)

        await channel.send(embed=embed, delete_after=120.0)
        return None

    if message.content.startswith("!설정 "):
        channel = message.channel
        value = message.content.replace("!설정 ", "", 1)
        try:
            int(value)
            value_list = []
            value_list.append(int(value[0]) - 1)
            value_list.append(int(value[1]) - 1)
            value_list.append(int(value[2]) - 1)
            value_list.append(int(value[3]) - 1)

            if not 0 <= int(value_list[0]) <= 3:
                msg = "잘못 된 타입 값 입니다."
                await channel.send(msg, delete_after=10.0)
                return None

            if not 0 <= int(value_list[1]) <= 2:
                msg = "잘못 된 속도 값 입니다."
                await channel.send(msg, delete_after=10.0)
                return None

            if not 0 <= int(value_list[2]) <= 2:
                msg = "잘못 된 볼륨 값 입니다."
                await channel.send(msg, delete_after=10.0)
                return None

            if not 0 <= int(value_list[3]) <= 1:
                msg = "잘못 된 반말 여부 값 입니다."
                await channel.send(msg, delete_after=10.0)
                return None

            if get_tts_mp3.upload_user_setting(message, value_list):
                msg = "설정 완료!"
                await channel.send(msg)
                return None

            else:
                msg = "서버 문제로 인해 설정하지 못했습니다."
                await channel.send(msg)
                return None

        except Exception as e:
            msg = "잘못 된 값을 입력하셨습니다."
            await channel.send(msg)
            return None

    if message.content == "!현재설정":
        channel = message.channel
        now_setting = get_tts_mp3.configure_setting_text(message)

        if len(now_setting) == 0:
            await channel.send('설정 값이 없습니다.')
            return None

        embed = discord.Embed(title="현재 설정 (카카오 API)")
        embed.add_field(name="타입", value=str(now_setting[0]), inline=False)
        embed.add_field(name="속도", value=str(now_setting[1]), inline=False)
        embed.add_field(name="볼륨", value=str(now_setting[2]), inline=False)
        embed.add_field(name="반말 여부 (\"안녕하세요\"라고 입력해도 \"안녕\"이라고 말함.)", value=str(now_setting[3]), inline=False)
        await channel.send("<@" + str(message.author.id) + "> 님의 현재 설정입니다.", embed=embed, delete_after=120.0)

    if message.content == "!나가기":
        channel = message.channel
        voice_list = client.voice_clients

        if len(voice_list) == 0:
            await channel.send('들어간 보이스 채널이 없습니다.', delete_after=10.0)
            return None
        else:
            await voice_list[0].disconnect(force=True)
            await channel.send('나가기 완료', delete_after=10.0)
            return None

    if message.content.startswith("!채팅"):
        channel = message.channel
        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        keyword = message.content.replace("!채팅", "", 1).replace(" ", "", 1)
        print(len(keyword))
        chat_list = inner_query.get_chat(keyword)

        if chat_list == "False":
            await channel.send("서버 문제로 인해 정보를 찾지 못 했습니다.")
            return None

        if len(keyword) == 0:
            msg = "최근 월드, 채널 채팅 내용입니다. (최근 10개)"
        else:
            msg = "찾으시는 \'{}\'에 관한 내용입니다. (최근 10개)".format(str(keyword))

        if len(chat_list) == 0:
            msg += "```열심히 찾아봤지만 데이터가 없네요.```"
        else:
            for i in chat_list:
                msg += i

        await channel.send(msg)
        return None

    if message.content.startswith("!"):
        channel = message.channel

        judge = judge_server(message, channel)
        if not judge == "True":
            await channel.send(judge)
            return None

        msg = inner_query.get_custom_query(message)

        if not msg == "False":
            await channel.send(msg)
            inner_query.log_upload("Other", message.content, message.author)
            return None
        else:
            return None

client.run(token)

