import pymysql
import sys
sys.path.append('d:/uploadGit/account_info')
import mysql_info as m_info
from werkzeug.security import generate_password_hash

pwd = generate_password_hash('test123')

conn = pymysql.connect(host='192.168.111.133', port=3306, user=m_info.account_c, passwd=m_info.password_c, database='flasky')
cur = conn.cursor()
cur.execute('insert into user(username, password_hash, email) values("%s", "%s", "%s")'%('sys', pwd ,'sys3948@naver.com'))
conn.commit()
cur.close()
conn.close()