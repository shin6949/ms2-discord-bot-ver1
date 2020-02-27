import time
import pymysql
import random

# 별도 파일
import public_SQL


def too_many_result():
    return "검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요."


def log_upload(message, querytype, respond):
    try:
        channel = message.channel.name

        try:
            conn = public_SQL.make_connection()
            curs = conn.cursor()
            # time, user, type, chat, Server, ServerID, ChannelName
            query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, %s, %s, %s)"
            curs.execute(query, (str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond), str(message.guild.name), str(message.guild.id), str(message.channel.name)))
            conn.commit()
            conn.close()

        except Exception as d:
            try:
                conn = public_SQL.make_backupconnection()
                curs = conn.cursor()
                # time, user, type, chat, Server, ServerID, ChannelName
                query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, %s, %s, %s)"
                curs.execute(query, (
                str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond),
                str(message.guild.name), str(message.guild.id), str(message.channel.name)))
                conn.commit()
                conn.close()
            except:
                print(d)

    except Exception as e:
        channel = "DM MODE"

        try:
            conn = public_SQL.make_connection()
            curs = conn.cursor()
            # time, user, type, chat, Server, ServerID, ChannelName
            query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, null, null, %s)"
            curs.execute(query, (str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond), channel))
            conn.commit()
            conn.close()

        except Exception as d:
            try:
                conn = public_SQL.make_backupconnection()
                curs = conn.cursor()
                # time, user, type, chat, Server, ServerID, ChannelName
                query = "insert into PublicVerLog values (now(), %s, %s, %s, %s, %s, null, null, %s)"
                curs.execute(query, (
                str(message.author), str(message.author.id), str(querytype), str(message.content), str(respond),
                channel))
                conn.commit()
                conn.close()
            except:
                print(d)


def chat_upload(message, checktype):
    try:
        channel = message.channel.name

        try:
            conn = public_SQL.make_connection()
            curs = conn.cursor()
            # time, user, type, chat, Server, ServerID, ChannelName
            query = "insert into Chat values (now(), %s, %s, %s, %s, %s, %s, %s)"
            curs.execute(query, (str(message.author), str(message.author.id), checktype, str(message.content), str(message.guild.name), str(message.guild.id), str(message.channel.name)))
            conn.commit()
            conn.close()

        except Exception as d:
            try:
                conn = public_SQL.make_backupconnection()
                curs = conn.cursor()
                # time, user, type, chat, Server, ServerID, ChannelName
                query = "insert into Chat values (now(), %s, %s, %s, %s, %s, %s, %s)"
                curs.execute(query, (
                str(message.author), str(message.author.id), checktype, str(message.content), str(message.guild.name),
                str(message.guild.id), str(message.channel.name)))
                conn.commit()
                conn.close()
            except:
                print(d)

    except Exception as e:
        channel = "DM MODE"

        try:
            conn = public_SQL.make_connection()
            curs = conn.cursor()
            # time, user, type, chat, Server, ServerID, ChannelName
            query = "insert into Chat values (now(), %s, %s, %s, %s, null, null, %s)"
            curs.execute(query, (
            str(message.author), str(message.author.id), checktype, str(message.content), str(channel)))
            conn.commit()
            conn.close()

        except Exception as d:
            try:
                conn = public_SQL.make_backupconnection()
                curs = conn.cursor()
                # time, user, type, chat, Server, ServerID, ChannelName
                query = "insert into Chat values (now(), %s, %s, %s, %s, null, null, %s)"
                curs.execute(query, (
                    str(message.author), str(message.author.id), checktype, str(message.content), str(channel)))
                conn.commit()
                conn.close()
            except:
                print(d)


def get_query_result(keyword):
    try:
        conn = public_SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = time.localtime()
        string = "%04d-%02d-%02d 00:00:00" % (now.tm_year, now.tm_mon, now.tm_mday)
        query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%" + keyword + "%' AND addtime < '" + string + "'"
        curs.execute(query)
        rows = curs.fetchall()

        if len(rows) > 30:
            return too_many_result()

        msg = "\"" + keyword + "\"에 대한 검색 결과: " + str(len(rows)) + "개"
        if len(rows) == 0:
            msg += "\n제보는 '!제보'"
            conn.close()
            return msg

        msg_list = []
        for i in rows:
            if i['answer'] == 0:
                msg_list.append("```\n[X] " + i['problem'] + "```")
            elif i['answer'] == 1:
                msg_list.append("```ini\n[O] " + i['problem'] + "\n```")

        for i in msg_list:
            msg += i

        conn.close()

        time.sleep(random.randrange(0, 3))
        return msg

    except Exception as e:
        try:
            conn = public_SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            now = time.localtime()
            string = "%04d-%02d-%02d 00:00:00" % (now.tm_year, now.tm_mon, now.tm_mday)
            query = "SELECT num, answer, problem FROM Problem WHERE problem LIKE '%" + keyword + "%' AND addtime < '" + string + "'"
            curs.execute(query)
            rows = curs.fetchall()

            if len(rows) > 30:
                return too_many_result()

            msg = "\"" + keyword + "\"에 대한 검색 결과: " + str(len(rows)) + "개"
            if len(rows) == 0:
                msg += "\n제보는 '!제보'"
                conn.close()
                return msg

            msg_list = []
            for i in rows:
                if i['answer'] == 0:
                    msg_list.append("```\n[X] " + i['problem'] + "```")
                elif i['answer'] == 1:
                    msg_list.append("```ini\n[O] " + i['problem'] + "\n```")

            for i in msg_list:
                msg += i

            conn.close()

            time.sleep(random.randrange(0, 3))
            return msg

        except:
            print(e)
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def get_boss(keyword, message, start):
    try:
        conn = public_SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM BossTable WHERE time = " + keyword
        curs.execute(query)
        rows = curs.fetchall()

        msg = "검색 결과: " + str(len(rows)) + "개\n새벽 시간대는 다를 수도 있으므로 게임에서 확인 바랍니다."
        msg_list = []

        for i in rows:
            msg_list.append("```\n이름: " + i['name'] + "\n레벨: " + str(i['level']) + "\n맵: " + i['map'] + "```")

        for i in msg_list:
            msg += i

        conn.commit()
        conn.close()

        return msg

    except Exception as e:
        try:
            conn = public_SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM BossTable WHERE time = " + keyword
            curs.execute(query)
            rows = curs.fetchall()

            msg = "검색 결과: " + str(len(rows)) + "개\n새벽 시간대는 다를 수도 있으므로 게임에서 확인 바랍니다."
            msg_list = []

            for i in rows:
                msg_list.append("```\n이름: " + i['name'] + "\n레벨: " + str(i['level']) + "\n맵: " + i['map'] + "```")

            for i in msg_list:
                msg += i

            conn.commit()
            conn.close()

            return msg

        except:
            print(e)
            msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
            return msg


def get_custom_query(message):
    try:
        conn = public_SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT Respond FROM PublicVerCustomRespond WHERE Command = '" + message.content + "'"
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
            conn = public_SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT Respond FROM PublicVerCustomRespond WHERE Command = '" + message.content + "'"
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

