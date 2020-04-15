import pymysql


def make_connection():
    # Azure
    conn = pymysql.connect(host='{DB_HOST}', user='OXBot', password='{DB_PASSWORD}', db='MS2OX', charset='utf8mb4',
                           connect_timeout=3)

    return conn


def make_chatonnection():
    # Azure
    conn = pymysql.connect(host='{DB_HOST}', user='OXBot', password='{DB_PASSWORD}', db='MS2_Black', charset='utf8mb4',
                           connect_timeout=3)

    return conn


def make_backupconnection():
    # Google Cloud
    conn = pymysql.connect(host='{DB_HOST}', user='OXBot', password='{DB_PASSWORD}', db='MS2OX', charset='utf8mb4',
                           connect_timeout=3)

    return conn
