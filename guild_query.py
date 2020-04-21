from datetime import datetime

import pymysql

# 별도 파일
import SQL
import Write_error_log


def return_location():
    return "GuildOXBot - guild_query.py"


def return_custom_msg(conn, message):
    curs = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT Respond FROM CustomRespond WHERE Command = '{}'".format(message.content)
    curs.execute(query)
    rows = curs.fetchall()

    if not len(rows) == 0:
        msg = rows[0]['Respond']
    else:
        msg = "False"

    return msg


def get_custom_query(message):
    try:
        conn = SQL.make_connection()
        msg = return_custom_msg(conn, message)
        if conn.open:
            conn.close()
        return msg

    except:
        try:
            conn = SQL.make_backupconnection()
            msg = return_custom_msg(conn, message)
            if conn.open:
                conn.close()
            return msg

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
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

        chatlist = []
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

            chatlist.append(tmp)

        conn.commit()
        conn.close()

        return chatlist

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return "False"
