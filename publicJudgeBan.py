import pymysql

# 별도 파일
import Write_error_log
import public_SQL


def check_user(conn, author_id): ...


def check_server(conn, guild_id): ...


def make_connection(): ...


def return_location():
    return "PublicOXBot - publicJudgeBan.py"


def judge(message):
    conn = make_connection()
    user_id = message.author.id

    # True 반환시 밴 당한 것
    if check_user(conn, user_id):
        if conn.open:
            conn.close()
        return True
    else:
        try:
            # 밴 당한 서버인지 체크
            guild_id = message.guild.id
            if check_server(conn, guild_id):
                if conn.open:
                    conn.close()
                return True
        # Guild ID 참조가 안되어, AttributeError가 발생하면 DM으로 보낸 것임.
        except AttributeError:
            if conn.open:
                conn.close()
            return False

        # 기타 에러가 생겼을 경우, 일단 보내 줌
        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
            print(e)
            if conn.open:
                conn.close()
            return False


def check_user(conn, author_id):
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT user_id FROM PublicBanList WHERE user_id = '{}'".format(str(author_id))
        curs.execute(query)
        rows = curs.fetchall()

        # 밴 유저가 아닌 경우
        if len(rows) == 0:
            return False
        # 밴 유저인 경우
        else:
            return True
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        print(e)
        return False


def check_server(conn, guild_id):
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT server_id FROM PublicBanServer WHERE server_id = '{}'".format(str(guild_id))
        curs.execute(query)
        rows = curs.fetchall()

        # 서버가 밴이 아니라면
        if len(rows) == 0:
            return False
        # 서버가 밴이라면
        else:
            return True
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        print(e)
        return False


def make_connection():
    try:
        conn = public_SQL.make_connection()
        return conn

    except TimeoutError as e:
        Write_error_log.write_log(return_location(), str(e))
        conn = public_SQL.make_backupconnection()
        return conn
