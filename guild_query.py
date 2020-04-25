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

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return "False"

