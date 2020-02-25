import pymysql


def make_connection():
    # Azure
    conn = pymysql.connect(host='{DB_HOST}', user='OXBot', password='{DB_PASSWORD}', db='MS2OX', charset='utf8mb4')

    return conn


def make_backupconnection():
    # Google Cloud
    conn = pymysql.connect(host='35.247.10.252', user='OXBot', password='{DB_PASSWORD}', db='MS2OX', charset='utf8mb4')

    return conn

