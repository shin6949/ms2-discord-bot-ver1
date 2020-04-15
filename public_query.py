import pymysql

import Write_error_log
# 별도 파일
import public_SQL


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

