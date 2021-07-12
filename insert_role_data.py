'''
Role Table에 데이터 삽입하기.
Role Table은 사용자의 권한 정보를 저장하는 Table이다.
권하는 총 5개가 존재한다.
1.FOLLOW = 1(팔로우 사용자)
2.COMMENT = 2(다른 사람들이 만든 글에 코멘트 달기)
3.WRITE = 4(글 작성)
4.MODERATE = 8(다른 사람이 작성한 코멘트 수정)
5.ADMIN = 16(관리자)

이 권한들을 조합하여 사용자에게 권한을 줄 것이다.
권한의 조합은 비트 연산자의 OR 연산을 사용하여 조합한다.

조합된 권하는 총 4개의 유형이다.
1.임의 : 0
2.사용자 : 7
3.수정자 : 15
4.관리자 : 16
'''

import pymysql
import sys
sys.path.append('d:/uploadGit/account_info')
import mysql_info as m_info


class Permission:
    F0LLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


def insert_roles():
    roles = {
        'User' : (Permission.F0LLOW | Permission.COMMENT | Permission.WRITE, 1),
        'Moderator' : (Permission.F0LLOW | Permission.COMMENT | Permission.WRITE | Permission.MODERATE, 1),
        'Administrator' : (Permission.ADMIN, 0)
    }
    conn = pymysql.connect(host='192.168.111.133', port=3306, user=m_info.account_c, passwd=m_info.password_c, database='flasky')
    cur = conn.cursor()
    for r in roles:
        if cur.execute("select * from role where name = '%s'" %(r)):
            cur.execute("update role set permissins = '%s', default_value = '%s' where name='%s'" %(roles[r][0], roles[r][1], r))
        else:
            cur.execute("insert into role(name, default_value, permissins) value('%s', '%s', '%s')" %(r, roles[r][1], roles[r][0]))
    conn.commit()
    cur.close()
    conn.close()
    return


if __name__ == '__main__':
    insert_roles()
