#Welcome to Fmuser

![](https://travis-ci.org/sudaning/Fmuser.svg?branch=master)
![](https://img.shields.io/pypi/v/pyFmuser.svg)
![](https://img.shields.io/badge/python-3.5-green.svg)
![](https://img.shields.io/badge/python-2.7-green.svg)
![](https://img.shields.io/badge/docs-stable-brightgreen.svg?style=flat)
![](https://img.shields.io/github/stars/sudaning/Fmuser.svg)
![](https://img.shields.io/github/forks/sudaning/Fmuser.svg)

##Introduction

Fmuser is a pure Python library designed to modify [FREESWITCH](https://freeswitch.org/)'s register user information in batch mode.
In [/scripts](https://github.com/sudaning/Fmuser/tree/master/scripts) , there are some scripts written by me for daily use.

##Installation
1. Via **pip**  
```pip install pyFmuser```  
2. Via **easy_install**  
```easy_install pyFmuser```  
3. From **source**(recommend)   
```python setup.py install```  

##upgrading
1. Via **pip**  
```pip install --upgrade pyFmuser```

##Examples
```python
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
```

##From the author
**Welcome to use Fmuser (●'◡'●)ﾉ♥**  
If you find any bug, please report it to me by opening a issue.
Fmuser needs to be improved, your contribution will be welcomed.



