#-*-coding:utf8 -*-...
import MySQLdb

conn = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="123456",
    db="core",
    charset="utf8"
    )

cur = conn.cursor()

#插入分组，如；1,成华区 2，武侯区
def insert_group():
    file = open(r'group.txt')
    for line in file:
        linelist = line.split(',')
        #print linelist[0],linelist[1]
        sql = "insert IGNORE into fenzu(group_id,group_name) values(%s,%s)"
        arg = int(str(linelist[0])),linelist[1]
        cur.execute(sql,arg)

#插入ip，账号，密码
def insert_server():
    file = open(r'serverip.txt')
    for line in file:
        linelist = line.split(',')
        print linelist[0],linelist[1],linelist[2],linelist[3],linelist[4]
        sql = "insert IGNORE into device(group_id,ipaddr,username,pwd,port_num) values (%s,%s,%s,%s,%s)"
        arg = int(str(linelist[0])),linelist[1],linelist[2],linelist[3],linelist[4]
        cur.execute(sql,arg)


if __name__ == "__main__":
    insert_group()
    insert_server()
    conn.commit()
    conn.close()
