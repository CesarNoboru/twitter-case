import logging
import json
import pymysql
import sys
import time
from secrets import get_secret
logger = logging.getLogger()
logger.setLevel(logging.INFO)
secrets = ''

sql1 = """
SELECT usr_name as name, usr_followers as followers
FROM users 
ORDER BY usr_followers DESC
LIMIT 10;
"""
sql2 = """
SELECT DATE_FORMAT(twt_created, '%Y-%m-%d %T.%f') as creation_date, count(*) as count
FROM tweets
GROUP BY hour( twt_created ) , day( twt_created )
ORDER BY Count DESC;
"""
sql3 = """
SELECT COUNT(*) as count, twt_lang as lang, (
   SELECT usr_local FROM users WHERE tweets.twt_user_id = users.usr_id
   ) as local
FROM tweets
WHERE twt_msg like '%{}%'
GROUP BY twt_lang, (
   SELECT usr_local FROM users WHERE tweets.twt_user_id = users.usr_id
   )
ORDER BY Count DESC;
"""

sqls = {
    'followers' : sql1,
    'hour' : sql2,
    'posts' : sql3
}
    
def panic_out(error):
    logger.error(f"msg='RDS error' error='{error}'")
    sys.exit(error)

def formatter(query, response):
    form = """
    {
        "query" : [
                
        ],
        "exec_time" : ''
    }
    """
    try:
        json_str = json.loads(form)
        if query == 'followers':
            qr = json_str['query']
            for line in response:
                ln = { 'name': line[0], 'followers':line[1] }
                qr.append(ln)
        if query == 'hour':
            qr = json_str['query']
            for line in response:
                ln = { 'creation_date': line[0], 'count':line[1] }
                qr.append(ln)
        if query == 'posts':
            qr = json_str['query']
            for line in response:
                ln = { 'count': line[0], 'lang':line[1], 'location':line[2] }
                qr.append(ln)
    except Exception as e:
        logger.error(f"msg='Formatter error' error={e}")
    
    return json_str


def run(query, tag):
    sql = sqls[query]
    if tag is not None:
        sql = sql.format(tag)
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
    logger.info(f"msg='Querying data' query='{query}' tag='{tag}'")
    start_time = time.time()
    try:
        cursor.execute(sql)
        response = cursor.fetchall()
        cursor.close()
        con.close()
        seconds = time.time() - start_time
        response = formatter(query, response)
        logger.info(f"msg='Query done' query='{query}' tag='{tag}' exec_time='{seconds:.2f}'")
        logger.info(f"msg='Disconnected from  RDS' db_host='{secrets['host']}' db='{secrets['dbname']}' db_user='{secrets['username']}'")
    except Exception as e:
        panic_out(e)
    return response
