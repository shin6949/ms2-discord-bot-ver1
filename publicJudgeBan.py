import pymysql
import public_SQL

# 별도 파일
import Write_error_log


def return_location():
    return "PublicOXBot - publicJudgeBan.py"


def judge(message):
    try:
        conn = public_SQL.make_connection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT user_id FROM PublicBanList WHERE user_id = '" + str(message.author.id) + "'"
        curs.execute(query)
        rows = curs.fetchall()
        
        # 밴 유저가 아닌 경우
        if len(rows) == 0:
            # 서버가 밴인지 확인
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT server_id FROM PublicBanServer WHERE server_id = '" + str(message.guild.id) + "'"
            curs.execute(query)
            rows = curs.fetchall()

            # 서버가 밴이 아니라면
            if len(rows) == 0:
                if conn.open:
                    conn.close()
                return False
            # 서버가 밴이라면
            else:
                if conn.open:
                    conn.close()
                return True
            
        # 밴 유저인 경우
        else:
            conn.close()
            return True

    except:
        try:
            conn = public_SQL.make_backupconnection()
            curs = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT user_id FROM PublicBanList WHERE user_id = '" + str(message.author.id) + "'"
            curs.execute(query)
            rows = curs.fetchall()

            # 밴 유저가 아닌 경우
            if len(rows) == 0:
                # 서버가 밴인지 확인
                curs = conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT server_id FROM PublicBanServer WHERE server_id = '" + str(message.guild.id) + "'"
                curs.execute(query)
                rows = curs.fetchall()

                # 서버가 밴이 아니라면
                if len(rows) == 0:
                    if conn.open:
                        conn.close()
                    return False
                # 서버가 밴이라면
                else:
                    if conn.open:
                        conn.close()
                    return True

            # 밴 유저인 경우
            else:
                conn.close()
                return True

        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))
            return False

