#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import smtplib
from email.mime.text import MIMEText

def sendmail(information, problem):
    mail_host = ''  #smtp服务器地址
    mail_user = ''   #填写邮箱用户名
    mail_pass = ''   #邮箱密码
    sender = '发送信箱'  
    receivers = ['收件信箱']  
    message = MIMEText(information,'plain','utf-8')     
    message['Subject'] = problem
    message['From'] = sender
    message['To'] = receivers[0]
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,25)
    smtpObj.login(mail_user,mail_pass) 
    smtpObj.sendmail(sender,receivers,message.as_string()) 
    smtpObj.quit()    


data = {}

with open("data.json","r") as fd:
    data=json.load(fd)
    
conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',data={'username':data['_u'],'password':data['_p']})
if result.status_code != 200:
    print('认证大失败')
    sendmail('认证失败了！', 'Error')
    exit()

# Submit
result = conn.get('https://xxcapp.xidian.edu.cn/ncov/wap/default/index')
if result.status_code != 200:
    print('获取页面大失败')
    sendmail('获取页面失败了，检查网络连接！','Error')
    exit()
predef = json.loads(re.search('var def = ({.*});',result.text).group(1))

if "dump_geo" in sys.argv:
    print(predef['geo_api_info'])
    sendmail('获取地址出现问题','Error')
    exit()

try:
    del predef['jrdqtlqk']
    del predef['jrdqjcqk']
except:
    pass
del data['_u']
del data['_p']
predef.update(data)

result = conn.post('https://xxcapp.xidian.edu.cn/ncov/wap/default/save',data=predef)
#print(result.text)
dict_ = eval(result.text)

if (dict_['m'] == '操作成功'):
    try:
        sendmail('成功填报今日疫情通','Success')
    except:
        pass
    print('成功发送邮件')
else:
    print("已经填报！")
