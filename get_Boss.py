import re
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


def get(message, mode):
    if message.content == "!필보" or message.content == "!필보 ":
        msg = "키워드를 입력해주세요. (ex. !필보 5)"
        return msg

    keyword = re.findall('\d+', message.content)[0]

    try:
        if mode == "Guild":
            conn = SQL.make_connection()
        else:
            conn = public_SQL.make_connection()
        msg = return_boss_msg(keyword, conn)
        return msg

    except:
        try:
            if mode == "Guild":
                conn = SQL.make_connection()
            else:
                conn = public_SQL.make_connection()
            msg = return_boss_msg(keyword, conn)
            return msg

        except Exception as e:
            Write_error_log.write_log(return_location(mode), str(e))
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def return_boss_msg(keyword, conn):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM BossTable WHERE time = %s"
    curs.execute(query, (keyword))
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
