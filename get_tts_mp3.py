import requests
import pymysql
from datetime import datetime, timedelta

# 별도 파일
import Write_error_log


def return_location():
    return "GuildOXBot - get_tts_mp3.py"


def configure_db():
    conn = pymysql.connect(host='{DB_HOST}', user='{DB_USER}', password='{DB_PASSWORD}',
                           db='TTS', charset='utf8mb4')
    return conn


def configure_backup_db():
    conn = pymysql.connect(host='{DB_HOST}', user='{DB_USER}', password='{DB_PASSWORD}',
                           db='TTS', charset='utf8mb4')
    return conn


def get_recent_use():
    try:
        conn = configure_db()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT usetime FROM log ORDER BY usetime DESC"
        curs.execute(query)
        rows = curs.fetchall()

        if datetime.now() - rows[0]['usetime'] > timedelta(minutes=30):
            conn.close()
            return True

        return False

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return True


def upload_log(message):
    try:
        conn = configure_db()
        backupconn = configure_backup_db()

        curs = conn.cursor()
        query = "insert into log values (now(), %s, %s, %s)"
        curs.execute(query, (str(message.author), str(message.author.id), str(message.content)))
        conn.commit()

        backupcur = backupconn.cursor()
        query = "insert into log values (now(), %s, %s, %s)"
        backupcur.execute(query, (str(message.author), str(message.author.id), str(message.content)))
        backupconn.commit()

        conn.close()
        backupconn.close()

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return True


def configure_setting_text(message):
    now_setting = get_user_setting(message)

    setting_list = []

    if len(now_setting) == 0:
        return setting_list

    if now_setting[0]['type'] == 0:
        setting_list.append("여성 차분한 낭독체")
    if now_setting[0]['type'] == 1:
        setting_list.append("남성 차분한 낭독체")
    if now_setting[0]['type'] == 2:
        setting_list.append("여성 밝은 대화체")
    if now_setting[0]['type'] == 3:
        setting_list.append("남성 밝은 대화체")

    if now_setting[0]['speed'] == 0:
        setting_list.append("느림")
    if now_setting[0]['speed'] == 1:
        setting_list.append("보통")
    if now_setting[0]['speed'] == 2:
        setting_list.append("빠름")

    if now_setting[0]['volume'] == 0:
        setting_list.append("0.7배")
    if now_setting[0]['volume'] == 1:
        setting_list.append("1.0배")
    if now_setting[0]['volume'] == 2:
        setting_list.append("1.4배")

    if now_setting[0]['tone'] == 0:
        setting_list.append("사용하지 않음")
    if now_setting[0]['tone'] == 1:
        setting_list.append("사용함")

    return setting_list


def get_user_setting(message):
    conn = configure_db()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM setting WHERE user_id = '" + str(message.author.id) + "'"
    curs.execute(query)
    now_setting = curs.fetchall()

    return now_setting


def configure_data_tag(message):
    now_setting = get_user_setting(message)
    data_tag = []

    if len(now_setting) == 0:
        data_tag.append("<speak><voice name=\"WOMAN_DIALOG_BRIGHT\">")
        data_tag.append("</voice></speak>")
        return data_tag

    data_tag.append("<speak>")

    # 여성 차분한 낭독체
    if now_setting[0]['type'] == 0:
        data_tag.append("<voice name=\"WOMAN_DIALOG_CALM\">")
    # 남성 차분한 낭독체
    if now_setting[0]['type'] == 1:
        data_tag.append("<voice name=\"MAN_READ_CALM\">")
    # 여성 밝은 대화체
    if now_setting[0]['type'] == 2:
        data_tag.append("<voice name=\"WOMAN_DIALOG_BRIGHT\">")
    # 남성 밝은 대화체
    if now_setting[0]['type'] == 3:
        data_tag.append("<voice name=\"MAN_DIALOG_BRIGHT\">")
    
    # 느림
    if now_setting[0]['speed'] == 0:
        data_tag.append("<prosody rate=\"slow\" ")
    # 보통
    if now_setting[0]['speed'] == 1:
        data_tag.append("<prosody rate=\"medium\" ")
    # 빠름
    if now_setting[0]['speed'] == 2:
        data_tag.append("<prosody rate=\"fast\" ")
    
    # 적게
    if now_setting[0]['volume'] == 0:
        data_tag.append("volume=\"soft\">")
    # 보통
    if now_setting[0]['volume'] == 1:
        data_tag.append("volume=\"medium\">")
    # 크게
    if now_setting[0]['volume'] == 2:
        data_tag.append("volume=\"loud\">")
    
    # 반말 모드 사용 X
    if now_setting[0]['tone'] == 0:
        data_tag.append("<kakao:effect tone=\"default\">")
    # 반말 모드 사용 O
    if now_setting[0]['tone'] == 1:
        data_tag.append("<kakao:effect tone=\"friendly\">")

    data_tag.append("</kakao:effect></prosody></voice></speak>")

    return data_tag


def upload_user_setting(message, value_list):
    # value_list Sample: [3, 2, 2, 2]
    try:
        if len(get_user_setting(message)) > 0:
            if update_user_setting(message, value_list):
                return True
            else:
                return False

        else:
            conn = configure_db()
            curs = conn.cursor()
            # user_id, user, settime, api, type, speed, volume, tone
            query = "insert into setting values (%s, %s, now(), %s, %s, %s, %s, %s)"
            curs.execute(query, (str(message.author.id), str(message.author.name), str("0"), str(value_list[0]), str(value_list[1]),
                                 str(value_list[2]), str(value_list[3])))
            conn.commit()
            conn.close()

            return True

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False


def update_user_setting(message, value_list):
    # value_list Sample: [3, 2, 2, 2]
    try:
        conn = configure_db()
        curs = conn.cursor()
        # user_id, user, settime, api, type, speed, volume, tone
        query = "UPDATE setting SET " \
                "type = " + str(value_list[0]) + ","\
                " speed = " + str(value_list[1]) + "," \
                " volume = " + str(value_list[2]) + "," \
                " tone = " + str(value_list[3]) + \
                " WHERE user_id = '" + str(message.author.id) + "'"

        curs.execute(query)
        conn.commit()
        conn.close()

        return True

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False


def get_kakao_mp3(message, keyword):
    try:
        url = 'https://kakaoi-newtone-openapi.kakao.com/v1/synthesize'

        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'KakaoAK {KAKAO_API_KEY}'
        }

        data_tag = configure_data_tag(message)

        if len(data_tag) == 2:
            byte_head = bytes(data_tag[0], encoding='utf-8')
            byte_keyword = bytes(keyword, encoding='utf-8')
            byte_tail = bytes(data_tag[1], encoding='utf-8')
        else:
            # data_tag = ['<speak>', '<voice name=\"(value)\">', '<prosody rate=(value) ', 'volume=(value)>', '<kakao:effect tone=(value)>, '</kakao:effect></prosody></voice></speak>']
            byte_head = bytes(str(data_tag[0] + data_tag[1] + data_tag[2] + data_tag[3] + data_tag[4]), encoding='utf-8')
            byte_keyword = bytes(keyword, encoding='utf-8')
            byte_tail = bytes(str(data_tag[5]), encoding='utf-8')

        data_str = byte_head + byte_keyword + byte_tail

        response = requests.post(url, headers=headers, data=data_str)
        f = open("result.mp3", "wb")
        f.write(response.content)
        f.close()

        return True
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False

