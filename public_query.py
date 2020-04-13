import time
import pymysql
import random

# 별도 파일
import public_SQL
import Write_error_log


def too_many_result():
    return "검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요."


# 서버에 로그를 업로드하는 코드
def log_upload(message, querytype, respond):
    conn = public_SQL.make_connection()

    try:
        curs = conn.cursor()
        # time, user, type, chat, Server, ServerID, ChannelName
        query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(query, (str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond), str(message.guild.name), str(message.guild.id), str(message.channel.name)))
        conn.commit()
        conn.close()
    
    # 에러가 나면 채널 쪽에서 에러가 난 것이라 DM일 것이라 추측할 수 있으므로 예외처리
    except:
        channel = "DM MODE"

        try:
            curs = conn.cursor()
            # time, user, type, chat, Server, ServerID, ChannelName
            query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, null, null, %s)"
            curs.execute(query, (str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond), channel))
            conn.commit()
            conn.close()

        except Exception as d:
            Write_error_log.write_log(d)

            # Connection이 열려있을 경우 닫는다.
            if conn.open:
                conn.close()


def return_ox_msg(conn, keyword):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now = time.localtime()
    string = "%04d-%02d-%02d 00:00:00" % (now.tm_year, now.tm_mon, now.tm_mday)
    query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%{}%' AND addtime < '{}'".format(keyword, string)
    curs.execute(query)
    rows = curs.fetchall()

    if len(rows) > 30:
        return too_many_result()

    msg = "\"{}\"에 대한 검색 결과: {}개".format(keyword, len(rows))
    if len(rows) == 0:
        msg += "\n제보는 '!제보'"
        conn.close()
        return msg

    msg_list = []
    for i in rows:
        if i['answer'] == 0:
            msg_list.append("```\n[X] {}```".format(i['problem']))
        elif i['answer'] == 1:
            msg_list.append("```ini\n[O] {}\n```".format(i['problem']))

    for i in msg_list:
        msg += i

    conn.close()
    return msg


def get_query_result(keyword):
    try:
        conn = public_SQL.make_connection()
        msg = return_ox_msg(conn, keyword)
        conn.close()
        time.sleep(random.randrange(0, 3))
        return msg

    except:
        try:
            conn = public_SQL.make_backupconnection()
            msg = return_ox_msg(conn, keyword)
            conn.close()
            return msg

        except Exception as e:
            Write_error_log.write_log(e)
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."

            return msg


def return_boss_msg(keyword, conn):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM BossTable WHERE time = {}".format(keyword)
    curs.execute(query)
    rows = curs.fetchall()

    msg = "검색 결과: {}개".format(len(rows))
    if len(rows) > 0:
        msg += "\n새벽 시간대는 다를 수도 있으므로 게임에서 확인 바랍니다."
    msg_list = []

    for i in rows:
        msg_list.append("```\n이름: {}\n레벨: {}\n맵: {}```".format(i['name'], i['level'], i['map']))

    for i in msg_list:
        msg += i

    return msg


def get_boss(keyword):
    try:
        conn = public_SQL.make_connection()
        msg = return_boss_msg(keyword, conn)
        conn.close()
        return msg

    except:
        try:
            conn = public_SQL.make_backupconnection()
            msg = return_boss_msg(keyword, conn)
            conn.close()
            return msg

        except Exception as e:
            Write_error_log.write_log(e)
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def return_custom_msg(message, conn):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT Respond FROM PublicVerCustomRespond WHERE Command = '{}'".format(message.content)
    curs.execute(query)
    rows = curs.fetchall()

    if not len(rows) == 0:
        msg = rows[0]['Respond']
    else:
        msg = "False"

    return msg


def get_custom_query(message):
    try:
        conn = public_SQL.make_connection()
        msg = return_custom_msg(message, conn)
        conn.close()

        return msg

    except:
        try:
            conn = public_SQL.make_backupconnection()
            msg = return_custom_msg(message, conn)
            conn.close()

            return msg

        except Exception as e:
            Write_error_log.write_log(e)
            return "False"

