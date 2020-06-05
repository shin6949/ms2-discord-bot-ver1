import pymysql


def make_connection():
    # Google Cloud
    conn = pymysql.connect(host='localhost', user='publicOX', password='{DB_PASSWORD}', db='MS2OX', charset='utf8mb4'
                           , connect_timeout=3)

    return conn

