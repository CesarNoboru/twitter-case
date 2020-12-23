import logging
import pymysql
import sys
import time
from secrets import get_secret
logger = logging.getLogger()
logger.setLevel(logging.INFO)
secrets = ''

def panic_out(error):
    logger.error(f"msg='RDS error' error='{error}'")
    sys.exit(error)

def clean(cursor):
    logger.info("msg='Cleaning the tables.'")
    sql = [
        "DROP TABLE IF EXISTS `tweets`;",
        "DROP TABLE IF EXISTS `users`;",
        "CREATE TABLE users (usr_id VARCHAR(255) PRIMARY KEY, usr_name VARCHAR(255), usr_user VARCHAR(255), usr_followers INTEGER, usr_local VARCHAR(255));",
        "CREATE TABLE tweets (twt_id VARCHAR(255) PRIMARY KEY, twt_user_id VARCHAR(255), twt_msg VARCHAR(255), twt_created DATETIME, twt_lang VARCHAR(255), FOREIGN KEY(twt_user_id) REFERENCES users(usr_id));"
    ]
    try:
        for s in sql:
            cursor.execute(s)
    except Exception as e:
        logger.error(f"msg='Error trying to clean tables' error='{e}'")
        sys.exit()
    return 0

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
        INSERT IGNORE INTO {} (
            {}
        )
        VALUES 
        {}
        
    """
    values = ""
    for line in list:
        value = "(#)"
        items = ''
        for item in line:
            item = str(item).replace('"', "'")
            item = "\"" + item + "\""
            if items == '':
                items = item
            else:
                items = items + ', ' + item
        value = value.replace('#', items)
        if values == '':
            values = value
        else:
            values = values + ', ' + value
    if type == "user":
        clean(cursor)
        logger.info(f"msg='Inserting Users to RDS' db_host='{secrets['host']}' db='{secrets['dbname']}' db_user='{secrets['username']}'")
        sql = sql.format("users", usr, values)
    else:
        logger.info(f"msg='Inserting Tweets to RDS' db_host='{secrets['host']}' db='{secrets['dbname']}' db_user='{secrets['username']}'")
        sql = sql.format("tweets", twt, values)
    start_time = time.time()
    try:
        cursor.execute(sql)
    except Exception as e:
        logger.error(f"msg='Error trying to INSERT' error='{e}'")
        sys.exit()
    seconds = time.time() - start_time
    logger.info(f"msg='Finished INSERT' type='{type}' exec_time='{seconds:.2f}'")
            
    return 0

def run(data):

    global secrets
    secrets = get_secret("twitter-case-db-cred")
    logger.info(f"msg='Trying to connect to RDS' db_host='{secrets['host']}' db='{secrets['dbname']}' db_user='{secrets['username']}'")
    
    try:
        con = pymysql.connect(
        user=secrets['username'],
        password=secrets['password'],
        host=secrets['host'],
        database=secrets['dbname']
        ) 
        cursor = con.cursor()
    except Exception as e:
        panic_out(e)
    logger.info(f"msg='Connected to RDS' db_host='{secrets['host']}' db='{secrets['dbname']}' db_user='{secrets['username']}'")

    insert(cursor, data[0], "user")
    insert(cursor, data[1], "tweet")

    try:
        cursor.close()
        con.commit()
        con.close()
        logger.info(f"msg='Commited to RDS' db_host='{secrets['host']}' db='{secrets['dbname']}' db_user='{secrets['username']}'")
    except Exception as e:
        panic_out(e)
    return 0
