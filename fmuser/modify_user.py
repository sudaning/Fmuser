#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import os
try: 
	import xml.etree.ElementTree as ET 
except ImportError: 
	import xml.etree.cElementTree as ET 
import HTMLParser

# 美化XML文件，缩进一致
def pretty_xml(elem, indent = "  ", newline = "\n", null_str_keep = True, level = 0):
	#print(level, len(elem), elem.text, elem.tail)
	i = newline + level * indent
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + indent
		for e in elem:
			pretty_xml(e, indent, newline, null_str_keep, level + 1)
		if not e.tail or not e.tail.strip():
			e.tail = (e.tail.count(newline) * newline + level * indent) if null_str_keep and e.tail else i
	if level and (not elem.tail or not elem.tail.strip()):
		elem.tail = (elem.tail.count(newline) * newline + level * indent) if null_str_keep and elem.tail else i
	if not len(elem) and elem.text:
		elem.text = elem.text.strip()
	return elem

class commentTreeBuilder(ET.XMLTreeBuilder):
	def __init__ (self, html = 0, target = None):
		ET.XMLTreeBuilder.__init__(self, html, target)
		self._parser.CommentHandler = self.handle_comment

	def handle_comment(self, data):
		self._target.start(ET.Comment, {})
		self._target.data(data)
		self._target.end(ET.Comment)

class Muser:
	'''
	<include>
	  <user id="075577010001">
	    <params>
	      <param name="password" value="33e9cloud"/>
	      <param name="vm-password" value="075577010001"/>
	    </params>
	    <variables>
	      <variable name="toll_allow" value="domestic,international,local"/>
	      <variable name="accountcode" value="075577010001"/>
	      <variable name="user_context" value="sipp.33e9.com"/>
	      <variable name="effective_caller_id_name" value="18688717887"/>
	      <variable name="effective_caller_id_number" value="18688717887"/>
	      <variable name="outbound_caller_id_name" value="$${outbound_caller_name}"/>
	      <variable name="outbound_caller_id_number" value="$${outbound_caller_id}"/>
	      <!-- <variable name="callgroup" value="techsupport"/> -->
	    </variables>
	  </user>
	</include>
	'''
	def __init__(self, user_dir=r'/usr/local/freeswitch/conf/directory', include_sub_dir=True, exclude_dir=[], debug=False):
		self.__user_dir = user_dir
		self.__include_sub_dir = include_sub_dir
		self.__exclude_dir = exclude_dir
		self.__modify_rule = {'key':r'/params/param[@name="password"]', 'value':''}
		self.__debug = debug

	def set_modify_rule(self, key=r'/params/param[@name="password"]', value=''): 
		self.__modify_rule = {'key':key, 'value':value}
		return self

	def __modfiy_xml(self, file_path, numbers=[]):
		tree = ET.parse(file_path, parser = commentTreeBuilder())
		include_node = tree.getroot() # include节点
		if self.__debug:
			print("TARGET %s" % file_path)
		user_node = include_node.find('user')
		if user_node is not None:
			id = user_node.attrib['id']
			if id in numbers or len(numbers) == 0:
				is_modify = False
				key_xpath = "./" + self.__modify_rule.get('key', '')
				value = self.__modify_rule.get('value', '')
				for node in include_node.findall(key_xpath):
					origion_value = node.get('value')
					node.set('value', value)
					is_modify = True
					print("MODIFY NODE %s ATTR 'value' FROM %s TO %s IN FILE %s" % (key_xpath, origion_value, value, file_path))
					break

				if is_modify:
					tree.write(file_path)

					# 读取文件内容，替换HTML的格式，重新写入
					with open(file_path, "r+") as f:
						txt = HTMLParser.HTMLParser().unescape(f.read())
						f.seek(0)
						f.truncate()
						f.write(txt)


	def run(self, numbers=[]):
		'''
		numbers = [] 代表不检查此条件
		'''
		for root, dirs, files in os.walk(self.__user_dir):					
			# 搜索当前目录下的所有xml文件 
			for file in files:
				if file[-3:] != "xml":
					continue
				self.__modfiy_xml(os.path.join(root, file), numbers)
			else:
				# 搜索完成，若不包含子目录，则直接break，不再继续搜索
				if not self.__include_sub_dir:
					break


