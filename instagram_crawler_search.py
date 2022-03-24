import urllib.request
import urllib.parse
import requests

from urllib.request import urlopen, Request
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import re
import json

import os
import time

from lxml import etree, html

from optparse import OptionParser

#parser = OptionParser()
#parser.add_option('-l', '--plearning',
#		action='store_true',
#		default=False,
#		help="print the processivity of learning",)
#
#
#(options, args) = parser.parse_args()
#
#if len(args) < 2:
#	print("Usage: python instagram_crawler_search.py {number of pictures you want per 1 tag} {tag1} {tag2} {tag3}.....")
#	exit()
#
#if args[0].isdigit() != True:
#	print("Argument Error: The first argument must be an integer")
#	exit()
#
#num_of_picture_in_one_tag = int(args[0])
#keywords = args[1:]
#
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

#with open('users', 'r') as userfp:
#	line = userfp.readline()
#	while line:
#		urls.append(line)
#		line = userfp.readline()
#

delimiter = '/'
phantomjs_path = "/Users/ftatp/Documents/Crawlers/phantomjs-2.1.1-macosx/bin/phantomjs"
chrome_path = "/home/ftatp/platform_tools/chromedriver"
#browser = webdriver.PhantomJS(phantomjs_path)
browser = webdriver.Chrome(chrome_path)
browser.set_window_size(1280, 1000)
browser.implicitly_wait(3)


login_url = "https://www.instagram.com/accounts/login/"

session = requests.session()

login_info = {
	"m_id": USER,
	"m_passwd": PASSWORD
}

browser.get(login_url)

login_div = browser.find_element_by_class_name("gr27e ")
elems = login_div.find_elements_by_class_name("_2hvTZ")
elems[0].send_keys(login_info['m_id'])
elems[1].send_keys(login_info['m_passwd'])

login_button = browser.find_element_by_tag_name("button")
login_button.click()

WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("coreSpriteDesktopNavLogoAndWordmark"))

print("Login Done")

browser.save_screenshot("clickupdate.png")
#
#for keyword in keywords:
#	browser.get("https://www.instagram.com/explore/tags/" + keyword)
#
#	WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("id8oV "))
#
#	browser.save_screenshot("clickupdate.png")
#	body = browser.find_element_by_tag_name("body")
#	main = browser.find_element_by_tag_name("main")
#
#	user_path = os.getcwd() + "/keyword/" + keyword
#
#	if not os.path.isdir(user_path):#user 폴더가 존재 하지 않으면
#		os.mkdir(user_path)
#
#	
#	# get picture panel
#	article = browser.find_element_by_class_name("KC1QD")
#
#	picture_list = []
#
##picture_panel = main.find_element_by_class_name(" _2z6nI")
#	i = 0
#
#	img_divs = article.find_elements_by_class_name("eLAPa")
#
#	a = []
#	for img_div in img_divs:
##browser.implicitly_wait(5)
#		if len(a) != 0:
#			print(a[0].get_attribute(innerHTML))
#			print(img_div.get_attribute(innerHTML))
#			print(a == img_div)
#
#		print(img_div.get_attribute("innerHTML"))
#		if i > num_of_picture_in_one_tag:
#			break
#		
#		# list of items
#		# 1. picture
#		# 2. picture's like list
#		# 3. number of comments
#		# 4. caption
#		# 5. location of the picture
#		# 6. date-time
#
#		picture = {
#			'owner': "",
#			'path': "",
#			'caption': "",
#			'tag_list': [],
#			'num_of_comments': 0,
#			'location': "",
##			'date_time': "",
##			'like_list': [],
#			'num_of_like': 0
#		}
#
#		path = ""
#		caption = ""
#		tag_list = []
#		comment_num = 0
#		like_list = []
#
#
#		# picture specific data
#		# click
#		img_click_div = img_div.find_element_by_class_name('_9AhH0')
#		img_click_div.click()
#		WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("M9sTE"))
#
#
##		article_tag = browser.find_element_by_class_name("M9sTE")
##		captiondiv = article_tag.find_element_by_class_name("eo2As")
##		ownerdiv = article_tag.find_element_by_class_name("Ppjfr")
##		
##		# Get picture owner
##		owner = ownerdiv.find_element_by_class_name('e1e1d')
##		picture['owner'] = owner.text
##
##		like_list = []	
##		try:
##			# click like list button and get like user list
##			like_span_tag = captiondiv.find_element_by_class_name("zV_Nj")
##			num_of_like = like_span_tag.text.split(' ')[0]
##		except Exception as e:
##			print(e)
##			print("Video")
##
##			# click x span
##			close_button = browser.find_element_by_class_name("ckWGn")
##			close_button.click()
##			continue
##	
##		#Like list, num
##		picture['num_of_like'] = num_of_like
##
##		i += 1
##
##		# location
##		try:
##			locationdiv = ownerdiv.find_element_by_class_name("M30cS")
##			location_tag = locationdiv.find_element_by_class_name("O4GlU")
##			location = location_tag.text
##		except:
##			location = ""
##
##		picture['location'] = location
##
##
##		
##		try:
##			text_ul_tag = captiondiv.find_element_by_tag_name("ul")
##
##
##			# caption, tag, comment_num
##			li_tags = text_ul_tag.find_elements_by_tag_name("li")
##			commenter_user_is_owner = True
##			for li_tag in li_tags:
##				caption += li_tag.text + '\n'
##				try:
##					text_board_a_tag = li_tag.find_element_by_tag_name("a")
##
##					if text_board_a_tag.get_attribute("title") == picture['owner'] and commenter_user_is_owner == True:
##						# li tag is a caption or tag
##						text_board_span_tag = li_tag.find_element_by_tag_name("span")
##						# print("Text: ", text_board_span_tag.get_attribute("innerHTML"))
##						# caption += text_board_span_tag.text
##						# get tags
##						tags = text_board_span_tag.find_elements_by_tag_name("a")
##						for tag in tags:
##							# print("Tag: ", tag.text)
##							if tag.text[0] == '#':
##								tag_list.append(tag.text)
###							try:
###								erase_pattern = re.compile(tag.text)
###								caption = re.sub(erase_pattern, '', caption)
###								#caption += ' '
###							except Exception as e:
###								print(e)
###
##
##					elif text_board_a_tag.get_attribute("title") != picture['owner']:
##						# li tag is a comment
##						# TODO: get all comments(if needed)
##						commenter_user_is_owner = False
##						comment_num += 1
##					else:
##						continue
##
##				except Exception as e: # Not possible
##					print("No <a> tag in this <li> tag")
##					print(e)
##
##			picture['caption'] = caption
##			picture['tag_list'] = tag_list
##			picture['num_of_comments'] = comment_num
##
##		except Exception as e:
##			print(e)
##			pass
##
###		# Date time
###		time_tag = captiondiv.find_element_by_tag_name("time")
###		date_time = time_tag.get_attribute("title")
###		picture['date_time'] = date_time
###
###		picture['like_list'] = like_list
##
#		# click x span
#		close_button = browser.find_element_by_class_name("ckWGn")
#		close_button.click()
#
#		img_divs = article.find_elements_by_class_name("eLAPa")
#		a.append(img_div)
#
#
##		# Get Picture
##		try:
##			img_src_div = img_div.find_element_by_class_name("KL4Bh")
##			print("dasda")
##			img_tag = img_src_div.find_element_by_tag_name("img")
##
##			img_link = img_tag.get_attribute("srcset")
##			print(img_link)
##			req = Request(url=img_link, headers=headers)
##			img = urlopen(req).read()
##		except:
##			print("failed to get picture\n")
##			continue
##
##		# picture path
##		picture_path = 'keyword' + delimiter + keyword  + delimiter + "picture" + str(i).zfill(4) + ".jpg"
##		with open(picture_path, mode='wb') as f:
##			f.write(img)
##			print("Saved...")
##
##		picture['path'] = picture_path
##
##		# data construction done
##		picture_list.append(picture)
##
###		# page down and repeat
###		if img_div == img_divs[len(img_divs) - 1]:
###			print("Scroll down\n\n")
###			body.send_keys(Keys.PAGE_DOWN)
###			time.sleep(1)
###			new_img_divs = picture_panel.find_elements_by_class_name("eLAPa")
###
###			idx = 0
###			for new_img_div in new_img_divs:
###				if new_img_div == img_div:
###					break
###				idx += 1
###
###			img_divs += new_img_divs[idx + 1:]
###
###
##		if i % 100 == 0:
##			print(picture_list)
##			with open("keyword" + delimiter + keyword + delimiter + "data" + str(i).zfill(4) + ".json", 'w') as fp:
##				json.dump(picture_list, fp)
##				picture_list = []
##			break
###user['picture_list'] = []
###
###
##	#build json
##	if len(picture_list) != 0:
##		with open("keyword" + delimiter + keyword + delimiter + "data" + str(i).zfill(4) + ".json", 'w') as fp:
##			json.dump(picture_list, fp)
##			picture_list = []
##
