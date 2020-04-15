from datetime import datetime, timedelta

import pymysql

import SQL
# 별도 파일
import Write_error_log


def return_location():
    return "Mini.py"


def get_recent_minigame():
    try:
        now = datetime.now() - timedelta(minutes=1)
        # string = "%02d:%02d:%02d" % (now.time().tm_hour, now.tm_min, now.tm_sec)
        time_str = now.strftime('%H:%M:%S')
        conn = SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM MiniGameTimeTable WHERE Time >= %s ORDER BY `Time` ASC"
        curs.execute(query, (str(time_str)))
        rows = curs.fetchall()

        if len(rows) == 0:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM MiniGameTimeTable ORDER BY `Time` ASC"
            curs.execute(query)
            rows = curs.fetchall()

        minigame_list = []

        # Game1: 0: OX, 1: 크레이지 러너즈, 2: 댄댄
        if str(rows[0]['Game1']) == "0":
            minigame_list.append("메이플 OX 퀴즈쇼")

        if str(rows[0]['Game1']) == "1":
            minigame_list.append("크레이지 러너즈")

        if str(rows[0]['Game1']) == "2":
            minigame_list.append("댄스댄스 스탑")

        # Game2: 0: 대탈출, 1: 스프링, 2: 트랩 마스터, 3: 파이널 서바이버
        if str(rows[0]['Game2']) == "0":
            minigame_list.append("루디브리엄 대탈출")

        if str(rows[0]['Game2']) == "1":
            minigame_list.append("스프링 비치")

        if str(rows[0]['Game2']) == "2":
            minigame_list.append("트랩 마스터")

        if str(rows[0]['Game2']) == "3":
            minigame_list.append("파이널 서바이버")

        # PvP: 0: 바르보사, 1: 피눈물, 2: 붉은 결투장
        if str(rows[0]['PvP']) == "0":
            minigame_list.append("바르보사 보물섬")

        if str(rows[0]['PvP']) == "1":
            minigame_list.append("피눈물 광산")

        if str(rows[0]['PvP']) == "2":
            minigame_list.append("붉은 결투장")

        time_string = str(rows[0]['Time']).replace(":", "시 ", 1).replace("00", "", -1).replace(":", "분", -1)

        msg = "제일 빠른 시간의 미니게임입니다.\n```시간: {}\n".format(str(time_string))

        for i in minigame_list:
            msg += i + "\n"

        msg += "```"

        if conn.open:
            conn.close()

        return msg

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        msg = "서버 이상으로 데이터를 갖고 올 수 없습니다."
        return msg
