#!/usr/bin/python

import paramiko
import psycopg2

evn = "10.10.94.148"
vtfe = "10.10.99.222"
mbnp = "10.10.99.130"
vpb = "10.10.154.100"
vpbbk = "10.10.154.101"
topcall1 = "10.10.94.34"
topcall2 = "10.10.92.110"
topcall3 = "10.10.94.140"
topcall4 = "10.10.92.117"
ops137 = "10.10.99.137"
sip94101 = "10.10.94.101"
sipbk = "10.10.99.138"

def gen_list():
	sql_list = []
	for data in open("blacklist_phone_num").readlines():
		if data != "":
			if len(data) == 11:
				data = data.strip()
				sql_list.append('''\
	INSERT INTO userblacklist(prefix,whitelist) VALUES {}\
	'''.format((data,0)))
	return sql_list

for server in (evn,vtfe,mbnp,vpb,vpbbk,topcall1,topcall2,topcall3,topcall4,ops137,sip94101,sipbk):
	try:
		conn = psycopg2.connect(
			database="opensips", 
			user='opensips', 
			password='opensipsrw', 
			host=server, 
			port= '5432'
		)
		conn.autocommit = True
		cursor = conn.cursor()

		for sql in gen_list():
			cursor.execute(sql)

		conn.commit()
		conn.close()
	except: pass

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
for server in (evn,vtfe,mbnp,vpb,vpbbk,topcall1,topcall2,topcall3,topcall4,ops137,sip94101,sipbk):
	try:
		ssh.connect(server, username="root", password="Pls@1234!")
		stdin,stdout,stderr = ssh.exec_command("opensipsctl fifo reload_blacklist")
	except: pass
