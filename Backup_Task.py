import pymysql
import datetime

# 외부 파일
import Write_error_log


def return_location():
    return "GuildOXBot - Backup_Task"


def backup_db():
    try:
        main_conn = pymysql.connect(host='{DB_HOST}', user='{DB_USER}', password='{DB_PASSWORD}', db='MS2OX',
                                    charset='utf8mb4')
        backup_conn = pymysql.connect(host='{DB_HOST}', user='{DB_USER}', password='{DB_PASSWORD}', db='MS2OX',
                                      charset='utf8mb4')
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False

    # 전날 오전 5시를 지정
    day = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d 05:00:00')
    curs = main_conn.cursor(pymysql.cursors.DictCursor)

    # 전날 오전 5시 ~ 오늘 오전 5시까지 불러옴
    query = "SELECT * FROM PublicVerLog WHERE usetime >= '{}'".format(str(day))
    curs.execute(query)
    rows = curs.fetchall()

    for data in rows:
        try:
            curs = backup_conn.cursor()
            # time, user, type, chat, Server, ServerID, ChannelName
            query = "insert into PublicVerLog values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            curs.execute(query, (data["usetime"], data["user"], data["user_id"], data["type"], data["chat"],
                                 data["respond"], data["Server"], data["SeverID"], data["ChannelName"]))
            backup_conn.commit()
        except Exception as e:
            Write_error_log.write_log(return_location(), str(e))

    # 한달전 5시를 지정
    month = (datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y-%m-%d 05:00:00')

    try:
        curs = main_conn.cursor()
        query = "DELETE FROM PublicVerLog WHERE usetime < '{}'".format(str(month))
        curs.execute(query)
        main_conn.commit()
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))

    main_conn.close()
    backup_conn.close()

    return True

