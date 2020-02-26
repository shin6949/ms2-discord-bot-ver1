import time
from datetime import datetime

import pymysql

# 별도 파일
import SQL


def log_upload(table, message, author):
    try:
        conn = SQL.make_connection()
        backupconn = SQL.make_backupconnection()

        curs = conn.cursor()
        query = "insert into " + table + " values (now(), %s, %s)"
        curs.execute(query, (str(message), str(author)))
        conn.commit()

        backupcursor = backupconn.cursor()
        query = "insert into " + table + " values (now(), %s, %s)"
        backupcursor.execute(query, (str(message), str(author)))
        backupconn.commit()

        conn.close()
        backupconn.close()

    except Exception as e:
        print(e)
        pass


def get_query_result(keyword, message, start):
    try:
        conn = SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%" + keyword + "%'"
        curs.execute(query)
        rows = curs.fetchall()

        msg = "\"" + keyword + "\"에 대한 검색 결과: " + str(len(rows)) + "개"

        msg_list = []
        for i in rows:
            if i['answer'] == 0:
                msg_list.append("```\n[X] " + i['problem'] + "```")
            elif i['answer'] == 1:
                msg_list.append("```ini\n[O] " + i['problem'] + "\n```")

        if str(message.author) == "COCOBLUE#7709":
            msg_list.append("\n연산 시간: " + str(time.time() - start))

        for i in msg_list:
            msg += i

        conn.commit()
        conn.close()

        return msg

    except Exception as e:
        try:
            conn = SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%" + keyword + "%'"
            curs.execute(query)
            rows = curs.fetchall()

            msg = "\"" + keyword + "\"에 대한 검색 결과: " + str(len(rows)) + "개"

            msg_list = []
            for i in rows:
                if i['answer'] == 0:
                    msg_list.append("```\n[X] " + i['problem'] + "```")
                elif i['answer'] == 1:
                    msg_list.append("```ini\n[O] " + i['problem'] + "\n```")

            if str(message.author) == "COCOBLUE#7709":
                msg_list.append("\n연산 시간: " + str(time.time() - start))

            for i in msg_list:
                msg += i

            conn.commit()
            conn.close()

            return msg

        except:
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def get_boss(keyword, message, start):
    try:
        conn = SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM BossTable WHERE time = " + keyword
        curs.execute(query)
        rows = curs.fetchall()

        msg = "검색 결과: " + str(len(rows)) + "개\n새벽 시간대는 다를 수도 있으므로 게임에서 확인 바랍니다."
        msg_list = []

        for i in rows:
            msg_list.append("```\n이름: " + i['name'] + "\n레벨: " + str(i['level']) + "\n맵: " + i['map'] + "```")

        print("time cal result")
        if str(message.author) == "COCOBLUE#7709":
            msg_list.append("\n연산 시간: " + str(time.time() - start))

        print("msg append")
        for i in msg_list:
            msg += i

        conn.commit()
        conn.close()

        return msg

    except Exception as e:
        try:
            conn = SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM BossTable WHERE time = " + keyword
            curs.execute(query)
            rows = curs.fetchall()

            msg = "검색 결과: " + str(len(rows)) + "개\n새벽 시간대는 다를 수도 있으므로 게임에서 확인 바랍니다."
            msg_list = []

            for i in rows:
                msg_list.append("```\n이름: " + i['name'] + "\n레벨: " + str(i['level']) + "\n맵: " + i['map'] + "```")

            print("time cal result")
            if str(message.author) == "COCOBLUE#7709":
                msg_list.append("\n연산 시간: " + str(time.time() - start))

            print("msg append")
            for i in msg_list:
                msg += i

            conn.commit()
            conn.close()

            return msg

        except:
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def get_custom_query(message):
    try:
        conn = SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT Respond FROM CustomRespond WHERE Command = '" + message.content + "'"
        curs.execute(query)
        rows = curs.fetchall()

        if not len(rows) == 0:
            msg = rows[0]['Respond']
        else:
            msg = "False"

        conn.commit()
        conn.close()

        return msg

    except Exception as e:
        try:
            conn = SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT Respond FROM CustomRespond WHERE Command = '" + message.content + "'"
            curs.execute(query)
            rows = curs.fetchall()

            if not len(rows) == 0:
                msg = rows[0]['Respond']
            else:
                msg = "False"

            conn.commit()
            conn.close()

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
