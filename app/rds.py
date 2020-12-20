from log import logger
import pymysql
import sys
import time
from secrets import get_secret

secrets = ''

def panic_out(error):
    logger.error(f"msg='RDS error' error='{error}'")
    sys.exit(error)

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
    secrets = get_secret()
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
