# 5분 전에 미니 게임을 사전 통보해주는 기능
import datetime
import re

import pymysql

import Write_error_log
import public_SQL


def return_location():
    return "PublicOXBot - minigamenoticeservice.py"


# 차단 등의 이유로 메시지를 전송할 수 없는 경우 리스트에서 삭제하는 함수
def error_handling(id_value, mode):
    conn = public_SQL.make_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)

    if mode == "Server":
        query = "DELETE FROM MiniGameNoticeService WHERE server_id = %s"
        curs.execute(query, id_value)
        conn.commit()
    else:
        query = "DELETE FROM MiniGameNoticeService WHERE requester = %s AND type = 1"
        curs.execute(query, id_value)
        conn.commit()

    if conn.open:
        conn.close()


# 기존에 등록되어 있는 항목을 삭제하는 함수
def delete_existing_status(conn, message, mode):
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 서버에서 등록을 요청하는 경우
        if mode == "Server":
            query = "DELETE FROM MiniGameNoticeService WHERE server_id = %s"
            curs.execute(query, message.guild.id)
            conn.commit()
            return True

        # DM으로 요청하는 경우
        else:
            query = "DELETE FROM MiniGameNoticeService WHERE requester = %s AND type = 1"
            curs.execute(query, message.author.id)
            conn.commit()
            return True

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False


# 등록하는 함수
def register_service(message):
    # 띄어 쓰기를 기준으로 list 구성
    query_list = message.content.split(' ')

    # 모든 필드를 채웠는지 검사
    if not len(query_list) == 3:
        return "모든 부분을 채우지 않은 것 같습니다. \'!알림설명\' 명령어를 통해 등록 방법을 확인하세요."

    # ??시 형태로 입력했을 수도 있으므로 숫자만 추출
    for i in range(1, 3):
        query_list[i] = int(re.findall("\d+", query_list[i])[0])

    # 0 ~ 24시까지의 범위인지 검사
    if not (0 <= query_list[1] < 24) or not (0 <= query_list[2] < 24):
        return "설정 에러!\n올바른 범위를 입력하지 않으셨습니다. 올바른 숫자의 범위는 0 ~ 23입니다."

    # 시작 시간이 끝 시간보다 나중인가 검사
    if query_list[1] > query_list[2]:
        return "설정 에러!\n시작 시간은 끝 시간보다 나중일 수 없습니다."

    # 등록 진행
    conn = public_SQL.make_connection()
    try:
        test = message.guild.id

        if not message.channel.permissions_for(message.author).administrator:
            return "이 기능은 관리자 외에는 설정할 수 없습니다."

        delete_existing_status(conn, message, "Server")
        curs = conn.cursor()
        query = "insert into MiniGameNoticeService(server_id, channel_id, requester, type, starttime, endtime) VALUES (%s, %s, %s, %s, %s, %s)"
        curs.execute(query, (message.guild.id, message.channel.id, message.author.id, 0, query_list[1], query_list[2]))
        conn.commit()
        if conn.open:
            conn.close()

        return "<@{}>님이 요청하신 서버 '{}'의 채널 '{}'에 {}시부터 {}시까지의 미니게임 5분전 알림 등록이 완료되었습니다." \
            .format(message.author.id, message.guild, message.channel, query_list[1], query_list[2])

    # Server ID 값을 찾을 수 없는 경우에는 DM으로 신청한 것임.
    except AttributeError:
        delete_existing_status(conn, message, "DM")
        curs = conn.cursor()
        query = "insert into MiniGameNoticeService(requester, type, starttime, endtime) VALUES (%s, %s, %s, %s)"
        curs.execute(query, (message.author.id, 1, query_list[1], query_list[2]))
        conn.commit()
        if conn.open:
            conn.close()

        return "<@{}>님이 요청하신 {}시부터 {}시까지의 미니게임 5분전 알림 등록이 완료되었습니다." \
            .format(message.author.id, query_list[1], query_list[2])


# 알림을 삭제하는 함수
def delete_alarm(message):
    conn = public_SQL.make_connection()

    try:
        server_id = message.guild.id
        if not message.channel.permissions_for(message.author).administrator:
            return "이 기능은 관리자 외에는 설정할 수 없습니다."

        if delete_existing_status(conn, message, "Server"):
            if conn.open:
                conn.close()

            return "정상적으로 삭제되었습니다."

        else:
            if conn.open:
                conn.close()

            return "서버 문제로 인해 삭제하지 못했습니다."

    # Server ID 값을 찾을 수 없는 경우에는 DM으로 신청한 것임.
    except AttributeError:
        if delete_existing_status(conn, message, "DM"):
            if conn.open:
                conn.close()

            return "정상적으로 삭제되었습니다."

        else:
            if conn.open:
                conn.close()

            return "서버 문제로 인해 삭제하지 못했습니다."


# 메시지를 보낼 사람, 서버(채널)를 찾는 함수
def get_subscriber():
    conn = public_SQL.make_connection()

    now_hour = datetime.datetime.now().hour
    # 1차적으로 서버와 채널을 갖고 옴.
    query = "SELECT server_id, channel_id FROM MiniGameNoticeService WHERE type = 0 AND starttime <= {} AND endtime >= {}".format(
        now_hour, now_hour)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()

    server = []
    for i in rows:
        server.append([i['server_id'], i['channel_id']])

    dm_list = []
    # 다음으로 DM 리스트를 갖고 옴.
    query = "SELECT requester FROM MiniGameNoticeService WHERE type = 1 AND starttime <= {} AND endtime >= {}".format(
        now_hour, now_hour)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute(query)
    rows = curs.fetchall()

    for i in rows:
        dm_list.append(i['requester'])

    return [server, dm_list]
