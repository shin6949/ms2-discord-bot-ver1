import datetime
import os
import pymysql

# 외부 파일
import Write_error_log


def return_location():
    return "GuildOXBot - Morning_Task.py"


def delete_log():
    # 30일 전 로그를 삭제
    try:
        main_conn = pymysql.connect(host='localhost', user='{DB_USER}', password='{DB_PASSWORD}', db='MS2OX',
                                    charset='utf8mb4')
    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False

    # 한달전 5시를 지정
    month = (datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y-%m-%d 05:00:00')

    try:
        curs = main_conn.cursor()
        query = "DELETE FROM log WHERE QueryTime < '{}'".format(str(month))
        curs.execute(query)
        main_conn.commit()

        # querynum을 정리
        query = "SET @COUNT = 0"
        curs.execute(query)
        main_conn.commit()

        query = "UPDATE log SET querynum = @COUNT:= @COUNT + 1"
        curs.execute(query)
        main_conn.commit()

    except Exception as e:
        Write_error_log.write_log(return_location(), str(e))
        return False

    if main_conn.open:
        main_conn.close()

    return True


# 다운로드한 프로필 사진, 길드 로고 삭제
def delete_png():
    path = "./"
    files = os.listdir(path)

    tmpcount = 0

    for file in files:
        tmp = "{}/{}".format(path, file)
        name, exten = os.path.splitext(tmp)

        if exten == ".png":
            if os.path.isfile(tmp):
                try:
                    os.remove(tmp)
                    tmpcount += 1

                except Exception as e:
                    Write_error_log.write_log(return_location(), str(e))
                    return False

    Write_error_log.write_log(return_location(), "{}개의 png 임시 파일을 삭제 완료".format(str(tmpcount)))
    return True


def doing_task():
    if not delete_log():
        Write_error_log.write_log(return_location(), str("Error Occurred"))
        return False

    if not delete_png():
        Write_error_log.write_log(return_location(), str("Error Occurred"))
        return False

    return True

