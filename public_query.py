import time
import pymysql

# 별도 파일
import public_SQL
import Write_error_log


def return_location():
    return "PublicOXBot - public_query.py"


def too_many_result():
    return "검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요."


def log_upload(message, querytype, respond):
    try:
        conn = public_SQL.make_connection()
        curs = conn.cursor()
        # time, user, type, chat, Server, ServerID, ChannelName
        query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(query, (str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond), str(message.guild.name), str(message.guild.id), str(message.channel.name)))
        conn.commit()
        conn.close()

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))


def return_ox_msg(conn, keyword):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now = time.localtime()
    string = "%04d-%02d-%02d 00:00:00" % (now.tm_year, now.tm_mon, now.tm_mday)
    query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%{}%' AND addtime < '{}'".format(keyword, string)
    curs.execute(query)
    rows = curs.fetchall()
    conn.close()

    if len(rows) == 0:
        msg = "\"{}\"에 대한 검색 결과가 없습니다.\n제보는 '!제보'".format(keyword)
        return msg
    elif len(rows) > 30:
        return too_many_result()
    else:
         msg = "\"{}\"에 대한 검색 결과: {}개".format(keyword, len(rows))

    msg_list = []
    for i in rows:
        if i['answer'] == 0:
            msg_list.append("```\n[X] {}```".format(i['problem']))
        elif i['answer'] == 1:
            msg_list.append("```ini\n[O] {}\n```".format(i['problem']))

    for i in msg_list:
        msg += i

    return msg


def get_query_result(keyword):
    try:
        conn = public_SQL.make_connection()
        msg = return_ox_msg(conn, keyword)
        if conn.open:
            conn.close()
        return msg

    except:
        try:
            conn = public_SQL.make_backupconnection()
            msg = return_ox_msg(conn, keyword)
            if conn.open:
                conn.close()
            return msg

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
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
        return msg

    except:
        try:
            conn = public_SQL.make_backupconnection()
            msg = return_boss_msg(keyword, conn)
            return msg

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
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
        if conn.open:
            conn.close()
        return msg

    except:
        try:
            conn = public_SQL.make_backupconnection()
            msg = return_custom_msg(message, conn)
            if conn.open:
                conn.close()
            return msg

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
            return "False"

