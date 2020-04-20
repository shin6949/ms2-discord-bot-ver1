import pymysql

import SQL
# 별도 파일
import Write_error_log
import public_SQL


def return_location(mode):
    if mode == "Public":
        return "PublicOXBot - OX_Quiz_Result.py"
    elif mode == "Guild":
        return "GuildOXBot - OX_Quiz_Result.py"
    else:
        return "Unknown Mode - OX_Quiz_Result.py"


def return_ox_msg(conn, keyword, mode):
    try:
        sql_keyword = keyword.replace("'", "''", keyword.count("'"))
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT answer, problem FROM Problem WHERE problem LIKE '%{}%' OR comment LIKE '%{}%'".format(
            sql_keyword, sql_keyword)
        curs.execute(query)
        rows = curs.fetchall()
        conn.close()

        if len(rows) == 0:
            if mode == "Guild":
                msg = "\"{}\"에 대한 검색 결과가 없습니다.\n코코블루에게 제보 부탁드려요.".format(keyword)
            else:
                msg = "\"{}\"에 대한 검색 결과가 없습니다.\n제보는 '!제보'".format(keyword)

            return msg

        elif len(rows) > 30:
            return "검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요."
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
    except Exception as e:
        Write_error_log.write_log(return_location(mode), str(e))
        print(e)
        return "서버 이상으로 데이터를 갖고 올 수 없습니다."


def configure_SQL(keyword, mode):
    try:
        if mode == "Guild":
            conn = SQL.make_connection()
        else:
            conn = public_SQL.make_connection()

        msg = return_ox_msg(conn, keyword, mode)

        if conn.open:
            conn.close()

        return msg

    except:
        try:
            if mode == "Guild":
                conn = SQL.make_connection()
            else:
                conn = public_SQL.make_connection()

            msg = return_ox_msg(conn, keyword, mode)

            if conn.open:
                conn.close()

            return msg

        except Exception as e:
            Write_error_log.write_log(return_location(mode), str(e))
            return "서버 이상으로 데이터를 갖고 올 수 없습니다."


def get(message, mode):
    keyword = message.content.replace("!ox ", "", 1) \
        .replace("!OX ", "", 1) \
        .replace("!퀴즈 ", "", 1) \
        .replace("!ㅋ ", "", 1) \
        .replace("!q ", "", 1) \
        .lstrip() \
        .rstrip()

    if len(keyword) < 2:
        msg = "검색어는 2글자 이상 입력해주세요."
        return msg

    msg = configure_SQL(keyword, mode)

    return msg
