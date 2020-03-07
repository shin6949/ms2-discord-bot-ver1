import time
from datetime import datetime

import pymysql

# 별도 파일
import SQL


def too_many_result():
    return "검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요."


def log_upload(table, message, author):
    try:
        conn = SQL.make_connection()
        backupconn = SQL.make_backupconnection()

        curs = conn.cursor()
        query = "insert into {} values (now(), %s, %s)".format(table)
        curs.execute(query, (str(message), str(author)))
        conn.commit()

        backupcursor = backupconn.cursor()
        query = "insert into {} values (now(), %s, %s)".format(table)
        backupcursor.execute(query, (str(message), str(author)))
        backupconn.commit()

        conn.close()
        backupconn.close()

    except Exception as e:
        print(e)
        pass


def return_ox_msg(conn, keyword, message, start):
    sql_keyword = keyword.replace("'", "''", keyword.count("'"))
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%{}%'".format(sql_keyword)
    curs.execute(query)
    rows = curs.fetchall()

    if len(rows) > 30:
        return too_many_result()

    msg = "\"{}\"에 대한 검색 결과: {}개".format(keyword, len(rows))

    msg_list = []
    for i in rows:
        if i['answer'] == 0:
            msg_list.append("```\n[X] {}```".format(i['problem']))
        elif i['answer'] == 1:
            msg_list.append("```ini\n[O] {}\n```".format(i['problem']))

    if str(message.author) == "COCOBLUE#7709":
        msg_list.append("\n연산 시간: {}".format(str(time.time() - start)))

    for i in msg_list:
        msg += i

    conn.commit()
    conn.close()

    return msg


def get_query_result(keyword, message, start):
    try:
        conn = SQL.make_connection()
        msg = return_ox_msg(conn, keyword, message, start)

        return msg

    except Exception as e:
        try:
            conn = SQL.make_backupconnection()
            msg = return_ox_msg(conn, keyword, message, start)

            return msg

        except:
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def return_boss_msg(conn, keyword, message, start):
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

    if str(message.author) == "COCOBLUE#7709":
        msg_list.append("\n연산 시간: {}".format(str(time.time() - start)))

    for i in msg_list:
        msg += i

    conn.commit()
    conn.close()
    return msg


def get_boss(keyword, message, start):
    try:
        conn = SQL.make_connection()
        msg = return_boss_msg(conn, keyword, message, start)

        return msg

    except Exception as e:
        try:
            conn = SQL.make_backupconnection()
            msg = return_boss_msg(conn, keyword, message, start)

            return msg

        except:
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def return_custom_msg(conn, message):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT Respond FROM CustomRespond WHERE Command = '{}'".format(message.content)
    curs.execute(query)
    rows = curs.fetchall()

    if not len(rows) == 0:
        msg = rows[0]['Respond']
    else:
        msg = "False"

    conn.commit()
    conn.close()
    return msg


def get_custom_query(message):
    try:
        conn = SQL.make_connection()
        msg = return_custom_msg(conn, message)

        return msg

    except Exception as e:
        try:
            conn = SQL.make_backupconnection()
            msg = return_custom_msg(conn, message)

            return msg
        except:
            print(e)
            return "False"


def get_chat(keyword):
    try:
        conn = SQL.make_chatonnection()
        curs = conn.cursor(pymysql.cursors.DictCursor)

        if len(keyword) == 0:
            query = "SELECT serverdate, Type, author, comment FROM new_chat ORDER BY serverdate DESC LIMIT 10"
            curs.execute(query)
        else:
            query = "SELECT serverdate, Type, author, comment FROM new_chat WHERE comment LIKE '%" + keyword + "%' ORDER BY serverdate DESC LIMIT 10"
            curs.execute(query)

        rows = curs.fetchall()

        list = []
        for i in range(len(rows) - 1, -1, -1):
            tmp = ""
            tmp += "```[" + rows[i]['serverdate'].strftime("%Y.%m.%d. %H:%M ")

            now = datetime.now()
            minus = now - rows[i]['serverdate']

            if minus.days == 0:
                if int(minus.seconds / 3600) == 0:
                    tmp += str(int(minus.seconds % 3600 / 60)) + "분 전]"
                else:
                    tmp += str(int(minus.seconds / 3600)) + "시간 " + str(int(minus.seconds % 3600 / 60)) + "분 전]"
            elif 1 <= minus.days <= 3:
                tmp += "약 " + str(minus.days) + "일 " + str(int(minus.seconds / 3600)) + "시간 전]"
            else:
                tmp += "약 " + str(minus.days) + "일 전]"

            if rows[i]['Type'] == 0:
                tmp += "[월드]"
            else:
                tmp += "[채널]"

            tmp += "\'{}\'의 채팅\n{}```".format(rows[i]['author'], rows[i]['comment'])

            print(tmp)

            list.append(tmp)

        print(len(list))
        conn.commit()
        conn.close()

        return list

    except Exception as e:
        print(e)
        return "False"
