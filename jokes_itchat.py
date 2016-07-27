# _*_ coding:utf-8 _*_
import sys
sys.path.append('C:/Users/LoveYing/Desktop')
import time
import itchat
import re
import urllib
import urllib.request
import getJoke from jokes 

#全局变量，生命在文件开头，笑话列表
joke_list = []

#抓取笑话，存储在joke_list中
j = getJoke()
for i in range(1, 5):
	j.url_tail = i
	joke_list += j.extractJoke()

#登录网页微信
itchat.auto_login()

#向微信号发送消息
@itchat.msg_register
def simple_reply(msg):
	if 'joke' in msg.get('Content', '') and len(joke_list) > 0:
		joke_return = joke_list[0].strip()
		#发送过的笑话及时删除
		joke_list.pop(0)	
		return joke_return
	elif len(joke_list) <= 0:
		return 'No more jokes!!!'
	else:
		return

itchat.run()