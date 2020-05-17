import pymysql

import Write_error_log
# 별도 파일
import public_SQL


def return_location():
    return "PublicOXBot - public_query.py"


def too_many_result():
    return "검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요."


def old_log_upload(message, querytype, respond):
    conn = public_SQL.make_connection()
    curs = conn.cursor()
    try:
        # time, user, type, chat, Server, ServerID, ChannelName
        query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(query, (
        str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond),
        str(message.guild.name), str(message.guild.id), str(message.channel.name)))
        conn.commit()
        conn.close()

    # DM으로 보낸 경우에는 서버 ID를 찾을 수 없어서 에러가 발생함.
    except AttributeError:
        # time, user, type, chat, Server, ServerID, ChannelName
        query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, null, null, null)"
        curs.execute(query, (
            str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond)))
        conn.commit()
        conn.close()

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        if conn.open:
            conn.close()


def upload_sql(query, content, respond):
    try:
        conn = public_SQL.make_connection()
        curs = conn.cursor()
        curs.execute(query, (content, respond))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        Write_error_log.write_log(return_location(), str(e))


# TODO: 로그 수집 거부 기능 완성해야함.
def log_upload(message, querytype, respond, processtime):
    try:
        # QueryTime, User_id, Query, Respond, Query_type, Query_from, Server_id, ProcessTime
        query = "insert into log(QueryTime, User_id, Query, Respond, Query_type, Query_from, Server_id, ProcessTime) values (now(), {}, %s, %s, '{}', {}, '{}', {})" \
            .format(str(message.author.id), querytype, str(1), str(message.guild.id), processtime)
        upload_sql(query, str(message.content), str(respond))
    # DM으로 보낸 경우에는 서버 ID를 찾을 수 없어서 에러가 발생함.
    except AttributeError:
        # QueryTime, User_id, Query, Respond, Query_type, Query_from, Server_id, ProcessTime
        query = "insert into log(QueryTime, User_id, Query, Respond, Query_type, Query_from, Server_id, ProcessTime) values (now(), {}, %s, %s, '{}', {}, null, {})" \
            .format(str(message.author.id), querytype, str(0), processtime)
        upload_sql(query, str(message.content), str(respond))

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        print(e)


def return_custom_msg(message, conn):
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT Respond FROM PublicVerCustomRespond WHERE Command = '{}'".format(message.content)
        curs.execute(query)
        rows = curs.fetchall()

        if not len(rows) == 0:
            msg = rows[0]['Respond']
        else:
            msg = "False"

        return msg
    except:
        return "False"


def get_custom_query(message):
    try:
        conn = public_SQL.make_connection()
        msg = return_custom_msg(message, conn)
        if conn.open:
            conn.close()
        return msg

    except Exception as e:
        return "False"

