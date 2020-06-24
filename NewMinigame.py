from datetime import datetime, timedelta

import discord
import pymysql

import SQL
# 별도 파일
import Write_error_log


def return_location():
    return "Mini.py"


def get_recent_minigame():
    now = datetime.now() - timedelta(minutes=1)
    return return_message(now)


def get_next_minigame():
    now = datetime.now() + timedelta(minutes=29)
    return return_message(now)


def return_message(now):
    try:
        # string = "%02d:%02d:%02d" % (now.time().tm_hour, now.tm_min, now.tm_sec)
        time_str = now.strftime('%H:%M:%S')
        conn = SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)

        query = """
        SELECT t.Time as time, n1.Name as game1, n2.Name as game2, n3.Name as pvp 
        FROM NewMiniTime as t
        LEFT JOIN MiniName as n1 ON t.Game1 = n1.GameNum
        LEFT JOIN MiniName as n2 ON t.Game2 = n2.GameNum
        LEFT JOIN MiniName as n3 ON t.PvP = n3.GameNum
        WHERE t.Time >= %s LIMIT 1;
        """

        curs.execute(query, (str(time_str)))
        rows = curs.fetchall()

        if len(rows) == 0:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = """
            SELECT t.Time as time, n1.Name as game1, n2.Name as game2, n3.Name as pvp 
            FROM NewMiniTime as t
            LEFT JOIN MiniName as n1 ON t.Game1 = n1.GameNum
            LEFT JOIN MiniName as n2 ON t.Game2 = n2.GameNum
            LEFT JOIN MiniName as n3 ON t.PvP = n3.GameNum
            ORDER BY t.Time ASC LIMIT 1;
            """
            curs.execute(query)
            rows = curs.fetchall()

        time_string = str(rows[0]['time']).replace(":", "시 ", 1).replace("00", "", -1).replace(":", "분", -1)

        embed = discord.Embed(title=time_string + " 미니게임", description="  ", color=0x00ff56)
        embed.add_field(name="첫 번째 미니게임", value=rows[0]['game1'], inline=False)
        embed.add_field(name="두 번째 미니게임", value=rows[0]['game2'], inline=False)
        embed.add_field(name="PvP", value=rows[0]['pvp'], inline=False)

        log = time_string + "{} 미니게임\n첫 번째 미니게임\n{}\n두 번째 미니게임\n{}\nPvP\n{}" \
            .format(time_string, rows[0]['game1'], rows[0]['game2'], rows[0]['pvp'])

        if conn.open:
            conn.close()

        result = {'status': 'success', 'message': embed, 'log': log}

        return result

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        result = {'status': 'error', 'message': "서버 이상으로 데이터를 갖고 올 수 없습니다."}
        return result
