#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
from fmuser import Muser

if __name__ == '__main__':
	# 搜索XML文件的根路径(递归搜索子路径)
	user_dir = '/usr/local/freeswitch/conf/directory'
	# XML中的路径
	key=r'/params/param[@name="password"]'
	# 需要修改的密码
	password = '1234'
	# 需要修改的用户号码
	numbers = ['1000', '13632672292', '2000']

	user = Muser(user_dir=user_dir)
	user.set_modify_rule(key=key, value=password)
	user.run(numbers)