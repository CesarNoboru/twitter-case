from env import read_env
from log import logger
import pymysql
import sys

DB_USER='twitterDbUser'
DB_PW='password-twitter-db'
DB_HOST='twitter-case-db.clezvho9gttj.us-east-1.rds.amazonaws.com'
DB='twitter_case_db'

def panic_out(error):
    logger.error(f"msg='RDS error' error='{error}'")
    sys.exit()

def insert(cursor, list, type):
    usr = """
            usr_id,
            usr_name,
            usr_user,
            usr_followers,
            usr_local
    """
    twt = """
            twt_id,
            twt_user_id,
            twt_msg,
            twt_created,
            twt_lang
        """
    sql = """ 
        INSERT INTO users (
            {}
        )
        VALUES (
            :1,
            :2,
            :3,
            :4,
            :5
        )
    """
    if type == "user":
        logger.info(f"msg='Inserting Users to RDS' db_host='{DB_HOST}' db='{DB}' db_user={DB_USER}")
        sql = sql.format(usr)
    else:
        logger.info(f"msg='Inserting Tweets to RDS' db_host='{DB_HOST}' db='{DB}' db_user={DB_USER}")
        sql = sql.format(twt).replace(":4", "STR_TO_DATE(:4, '%Y-%m-%dT%h:%m:s' )")
    try:
        cursor.execute(sql, list)
    except Exception as e:
        logger.error(f"msg='Error trying to INSERT' error='{e}'")
        return -1
    return 0

def run(data):
    logger.info(f"msg='Trying to connect to RDS' db_host='{DB_HOST}' db='{DB}' db_user={DB_USER}")
    try:
        con = pymysql.connect(
        user=DB_USER,
        password=DB_PW,
        host=DB_HOST,
        database=DB
        ) 
        cursor = con.cursor()
    except Exception as e:
        panic_out(e)
    logger.info(f"msg='Connected to RDS' db_host='{DB_HOST}' db='{DB}' db_user={DB_USER}")

    insert(cursor, data[0], "user")
    insert(cursor, data[1], "twt")

    try:
        cursor.close()
        con.commit()
        con.close()
    except Exception as e:
        panic_out(e)
    return 0
