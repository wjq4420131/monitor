# -*-coding:utf8 -*-...
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import json
import paramiko
import MySQLdb
import time


conn = MySQLdb.Connect(
    host="localhost",
    user="root",
    passwd="123456",
    db="core",
    charset="utf8"
)
cur = conn.cursor()

"""
全局静态数据
"""

user = "wangjinquan"  #
corpid = 'wx4b1207e05b64a7e9'  # CorpID是企业号的标识
# content="告警信息"
# corpsecretSecret是管理组凭证密钥
corpsecret = 'pFdQQNDBtFHTw8c_hYAqI8cbi-dQaaAKqZq-WaUEvusuKAN9lRjxO0ZOW0iUeiNK'


def get_ip():
    sql = "select ipaddr,username,pwd,port_num,group_id from device"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        ip = row[0]
        username = row[1]
        pwd = row[2]
        port_num = row[3]
        group_id = row[4]
        connect_server(ip, username, pwd, port_num,group_id)


def connect_server(ip, username, pwd, port_num,group_id):
    print ip,username,pwd,port_num,group_id
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port_num, username, pwd, timeout=20)

        """显示返回结果使用内存"""
        # 使用内存
        stdin, stdout1, stderr = ssh.exec_command(
            "free -m |awk 'NR==2' |awk '{ print $3}'")
        out1 = stdout1.readlines()
        print out1[0]

        # 剩余内存
        stdin, stdout2, stderr = ssh.exec_command(
            "free -m |awk 'NR==2' |awk '{ print $4}'")
        out2 = stdout2.readlines()
        print out2[0]

        # 使用交换分区
        stdin, stdout3, stderr = ssh.exec_command(
            "free -m |awk 'NR==3' |awk '{ print $3}'")
        out3 = stdout3.readlines()
        print out3[0]

        # 剩余交换分区
        stdin, stdout4, stderr = ssh.exec_command(
            "free -m |awk 'NR==3' |awk '{ print $4}'")
        out4 = stdout4.readlines()
        print out4[0]

        # 主机名称
        stdin, stdout5, stderr = ssh.exec_command("hostname")
        out5 = stdout5.readlines()
        print out5[0]

        # 执行获取cpu命令
        stdin, stdout6, stderr = ssh.exec_command("chmod -R 777 /home/get_cpu.sh")

        # 返回cpu结果
        stdin, stdout7, stderr = ssh.exec_command("/home/get_cpu.sh")
        out7 = stdout7.readlines()
        print out7[0]

        # 剩余cpu
        cpu = 100
        surplus_cpu = cpu-float(str(out7[0]))
        print surplus_cpu

        # 读取数量
        stdin, stdout8, stderr = ssh.exec_command(
            "vmstat |awk 'NR==3' |awk '{print $9}'")
        out8 = stdout8.readlines()
        print out8[0]

        # 硬盘写入数量
        stdin, stdout9, stderr = ssh.exec_command(
            "vmstat |awk 'NR==3' |awk '{print $10}'")
        out9 = stdout9.readlines()
        print out9[0]

        # 录像计划数
        stdin, stdout10, stderr = ssh.exec_command(
            "tail -n 5 /home/storeserver3.2/state.txt |head -n 1 | awk 'NR==1' | awk '{ print $1}' |cut -d: -f 2")
        out10 = stdout10.readlines()
        print out10[0]

        # 要存的数量
        stdin, stdout11, stderr = ssh.exec_command(
            "tail -n 5 /home/storeserver3.2/state.txt |head -n 1 | awk 'NR==1' | awk '{ print $2}' |cut -d: -f 2")
        out11 = stdout11.readlines()
        print out11[0]

        # 实际存储数
        stdin, stdout12, stderr = ssh.exec_command(
            "tail -n 5 /home/storeserver3.2/state.txt |head -n 1 | awk 'NR==1' | awk '{ print $3}' |cut -d: -f 2")
        out12 = stdout12.readlines()
        print out12[0]

        # core文件个数
        stdin, stdout13, stderr = ssh.exec_command(
            """ find /home/storeserver/ -name "core.*" | wc -l """)
        out13 = stdout13.readlines()
        print out13[0]

        # 文件赋权
        stdin, stdout14, stderr = ssh.exec_command("chmod -R 777 /home/network.sh")

        # 获取网卡
        stdin, stdout15, stderr = ssh.exec_command("/home/network.sh eth0")
        out15 = stdout15.readlines()
        print out15

        # 插入时间
        time_date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print time_date


        #进程
        stdin, stdout17, stderr = ssh.exec_command(
            "ps -ef|grep StoreServer |grep -v grep |awk 'NR==1' |awk '{ print $8}' ")
        out17 = stdout17.readlines()
        out17 = ''.join(out17)
        print out17

        # 版本
        stdin, stdout16, stderr = ssh.exec_command(
            "cat /home/storeserver3.2/Version |sed s/[[:space:]]/-/g")
        out16 = stdout16.readlines()
        print out16[0]


        sql = "insert into core_data(ip,used_men,surplus_men,used_swap,surplus_swap,hostname,used_cpu,disk_read,disk_write,Schemes,Records,Channels,core_number,log_data,network_in,network_out,surplus_cpu,app_version,app_process) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        arg = ip,out1[0],out2[0],out3[0],out4[0],out5[0],out7[0],out8[0],out9[0],out10[0],out11[0],out12[0],out13[0],time_date,out15[1],out15[2],surplus_cpu,out16[0],out17
        cur.execute(sql, arg)

        if int(out2[0]) < 30 or int(out4[0]) < 100:
            content="内存使用过高"
            sql= r"insert into waring(device_id,group_id,content,create_time,alarm_type) values(%s,%s,%s,%s,%s)"
            arg = ip,group_id,content,time_date,1 
            cur.execute(sql,arg)        
            send_msg(ip + ":"+ "内存使用过高" +  time_date)

        if float(out7[0]) > float(90.0):
            content="cpu使用过高"
            sql= r"insert into waring(device_id,group_id,content,create_time,alarm_type) values(%s,%s,%s,%s,%s)"
            arg = ip,group_id,content,time_date,1
            cur.execute(sql,arg)
            send_msg(ip + ":" + "cpu使用过高" + time_date)

        if out17 =="":
            content="进程丢失"
            sql= r"insert into waring(device_id,group_id,content,create_time,alarm_type) values(%s,%s,%s,%s,%s)"
            arg = ip,group_id,content,time_date,2
            cur.execute(sql,arg)
            send_msg(ip +":" +"进程丢失"+  time_date)
            

            ssh.close()

    except IOError,e:
        time_date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sql= "insert into waring(device_id,group_id,content,create_time,alarm_type) values(%s,%s,%s,%s,%s)"
        content="设备不通"
        arg = ip,group_id,content,time_date,2
        cur.execute(sql,arg)
        send_msg(ip + ":" +"设备不通" + time_date)


def gettoken(corpid, corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    token_file = urllib2.urlopen(gettoken_url)
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    return token_json['access_token']


def senddata(access_token, user, content):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser": user,  # 企业号中的用户帐号
        "toparty": "1",  # 企业号中的部门id
        "msgtype": "text",  # 消息类型。
        "agentid": "0",  # 代理id
        "text": {
            "content": content
        },
        "safe": "0"
    }

    send_data = json.dumps(send_values, ensure_ascii=False)
    send_request = urllib2.Request(send_url, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print str(response)


def send_msg(content):
    print content
    senddata(gettoken(corpid, corpsecret), user, content)


if __name__ == "__main__":
    get_ip()
    conn.commit()
    conn.close()
