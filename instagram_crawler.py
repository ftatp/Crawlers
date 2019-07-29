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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

ubuntu_delimiter = "/"
win_delimiter = "\\"

delimiter = win_delimiter

phantomjs_path = "/home/ftatp/platform_tools/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
chrome_path = "/home/ftatp/platform_tools/chromedriver"
#browser = webdriver.PhantomJS(phantomjs_path)

browser = webdriver.Chrome(chrome_path)
browser.set_window_size(1280, 1000)
browser.implicitly_wait(3)


test_urls = ["ftatp5901/"]
urls =[
 'ftatp5901',
 ]


for url in urls:
	browser.get("https://www.instagram.com/" + url)

	WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("oJZym")) #Wait until the logo appears


	# get user's id
	# list of id contents
	# 1. profile
	# 2. number of followers
	# 3. number of followings

	user = {
		'id': "",
		'num_of_followers': 0,
		'num_of_followings': 0,
		'picture_list': []
	}

	body = browser.find_element_by_tag_name("body")
	main = browser.find_element_by_tag_name("main")

	picture_panel = main.find_element_by_class_name(" _2z6nI")
	header = main.find_element_by_tag_name("header")

	nickname_tag = header.find_element_by_class_name("_7UhW9")
	nickname = nickname_tag.get_attribute("innerHTML")
	user['id'] = nickname
	user_path = os.getcwd() + delimiter + nickname

	if not os.path.isdir(user_path):#user 폴더가 존재 하지 않으면
		os.mkdir(user_path)

	#####################################################################################
	######        User follower, following, posting number
	id_content_table = header.find_element_by_tag_name("ul")
	li_tags = id_content_table.find_elements_by_tag_name("li")

	for li_tag in li_tags:
		try:
			a_tag = li_tag.find_element_by_tag_name("a")
		except:
			continue

		li_text = a_tag.text

		li_text_split = li_text.split(' ')
		if li_text_split[1] == "followers":
			user['num_of_followers'] = li_text_split[0]
			print("followers: " + user['num_of_followers'])

		if li_text_split[1] == "following":
			user['num_of_followings'] = li_text_split[0]
			print("followering: " + user['num_of_followings'])

	######################################################################################
	######         get picture panel
	article = browser.find_element_by_class_name("_2z6nI")

	picture_list = []

	i = 0

	img_divs = article.find_elements_by_class_name("eLAPa")

	for img_div in img_divs:
		if i > 300:
			break

		# list of items
		# 1. picture
		# 2. picture's like list
		# 3. number of comments
		# 4. caption
		# 5. location of the picture
		# 6. date-time

		picture = {
			'path': "",
			'caption': "",
			'tag_list': [],
			'num_of_comments': 0,
			'location': "",
			'date_time': "",
			#'like_list': [],
			'num_of_like': 0
		}

		path = ""
		caption = ""
		tag_list = []
		comment_num = 0
		like_list = []

		img_div.click()
		WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("M9sTE"))

		article_tag = browser.find_element_by_class_name("M9sTE")
		captiondiv = article_tag.find_element_by_class_name("eo2As")

		###########################################################
		#######    Get like number
		try:
			print("\n")
			like_tag = captiondiv.find_element_by_class_name("Nm9Fw")
			like_span_tag = like_tag.find_element_by_tag_name("span")
			num_of_like = like_span_tag.get_attribute("innerHTML")
			print("num of like: " + num_of_like)

		except:
			print("Video")

			# click x span
			close_button = browser.find_element_by_class_name("ckWGn")
			close_button.click()
			############################################################
			#######    Scroll down and repeat
			if img_div == img_divs[len(img_divs) - 1]:
				##print("Scroll down\n\n")
				body.send_keys(Keys.PAGE_DOWN)
				time.sleep(1)
				new_img_divs = picture_panel.find_elements_by_class_name("eLAPa")

				idx = 0
				for new_img_div in new_img_divs:
					if new_img_div == img_div:
						break
					idx += 1

				img_divs += new_img_divs[idx + 1:]



			continue

		#Like list, num
		picture['num_of_like'] = num_of_like

		i += 1

		############################################################
		#######    Get location
		try:
			locationdiv = ownerdiv.find_element_by_class_name("M30cS")
			location_tag = locationdiv.find_element_by_class_name("O4GlU")
			location = location_tag.text
		except:
			location = ""

		#Location
		picture['location'] = location


		############################################################
		#######    Date time
		time_tag = captiondiv.find_element_by_tag_name("time")
		date_time = time_tag.get_attribute("title")
		picture['date_time'] = date_time


		############################################################
		#######    Get caption, tags, comment number
		try:
			text_ul_tag = captiondiv.find_element_by_tag_name("ul")
			#li_tags = text_ul_tag.find_elements_by_tag_name("li")
			li_tags = text_ul_tag.find_elements_by_class_name("C4VMK")
			commenter_user_is_owner = True
			for li_tag in li_tags:
				commenter_atag = li_tag.find_element_by_class_name("TlrDj")
				commenter_spantag = li_tag.find_element_by_tag_name("span")
				#print(commenter_atag.text + "\n######################################")
				#print("######################################\n" + commenter_spantag.text + "\n######################################")
				whole_comment = commenter_atag.text + ' ' + commenter_spantag.text
				caption += whole_comment + '\n'

		# 	commenter_user_is_owner = True
		# e	for li_tag in li_tags:
		# 		caption += li_tag.text + '\n'
				try:
					text_board_a_tag = li_tag.find_element_by_tag_name("a")

					if text_board_a_tag.get_attribute("title") == user['id'] and commenter_user_is_owner == True:
						# li tag is a caption or tag
						text_board_span_tag = li_tag.find_element_by_tag_name("span")
						tags = text_board_span_tag.find_elements_by_tag_name("a")
						for tag in tags:
							#print("Tag: ", tag.text)
							if tag.text[0] == '#':
								tag_list.append(tag.text)

					elif text_board_a_tag.get_attribute("title") != user['id']:
						# li tag is a comment
						# TODO: get all comments(if needed)
						commenter_user_is_owner = False
						comment_num += 1
					else:
						continue

				except Exception as e: # Not possible
					print("No <a> tag in this <li> tag")
					print(e)
					pass

			# caption, tag, comment_num
			picture['caption'] = caption
			picture['tag_list'] = tag_list
			picture['num_of_comments'] = comment_num

		except Exception as e:
			print(e)
			pass

		##############################################################
		#######    close picture detail
		close_button = browser.find_element_by_class_name("ckWGn")
		close_button.click()


		############################################################
		#######    Save picture
		try:
			img_src_div = img_div.find_element_by_class_name("KL4Bh")
			img_tag = img_src_div.find_element_by_tag_name("img")

			img_link = img_tag.get_attribute("src")
			req = Request(url=img_link, headers=headers)
			img = urlopen(req).read()
		except:
			print("failed to get picture\n")
			continue

		# picture path
		picture_path = user_path + delimiter + "picture" + str(i).zfill(4) + ".jpg"
		with open(picture_path, mode='wb') as f:
			f.write(img)
			path = user['id'] + delimiter + "picture" + str(i).zfill(4) + ".jpg"
			print("Saved...")

		# picture path
		picture['path'] = path
		############################################################
		#######    Construct picture list
		picture_list.append(picture)


		############################################################
		#######    Scroll down and repeat
		if img_div == img_divs[len(img_divs) - 1]:
			##print("Scroll down\n\n")
			body.send_keys(Keys.PAGE_DOWN)
			time.sleep(1)
			new_img_divs = picture_panel.find_elements_by_class_name("eLAPa")

			idx = 0
			for new_img_div in new_img_divs:
				if new_img_div == img_div:
					break
				idx += 1

			img_divs += new_img_divs[idx + 1:]


		############################################################
		#######    Save picture information
		if i % 100 == 0:
			with open(user['id'] + delimiter + "data" + str(i).zfill(4) + ".json", 'w') as fp:
				user['picture_list'] = picture_list
				json.dump(user, fp, indent=4)
				picture_list = []
				user['picture_list'] = []

		############################################################

		print(picture)

	print(user['id'] + " Done")

	# build json
	user['picture_list'] = picture_list
	if len(user['picture_list']) != 0:
		with open(user['id'] + delimiter + "data" + str(i).zfill(4) + ".json", 'w') as fp:
			json.dump(user, fp, indent=4)
			picture_list = []
	######################################################################################









#login_url = "https://www.instagram.com/accounts/login/"
#
#USER = "ftatp5901@gmail.com"
#PASS = "egoism1950"
#
#session = requests.session()
#
#login_info = {
#	"m_id": USER,
#	"m_passwd": PASS
#}
#
#browser.get(login_url)
#
#login_div = browser.find_element_by_class_name("gr27e ")
#elems = login_div.find_elements_by_class_name("_2hvTZ")
#elems[0].send_keys(login_info['m_id'])
#elems[1].send_keys(login_info['m_passwd'])
#
#login_button = browser.find_element_by_class_name("L3NKy")
#login_button.click()
#
#WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("glyphsSpriteApp_instagram__outline__24__grey_9"))
#
#browser.save_screenshot("clickupdate.png")
#
#print("Login Done")















#		# picture specific data
#		try:
#			article_tag = browser.find_element_by_class_name("M9sTE")
#			captiondiv = article_tag.find_element_by_class_name("eo2As")
#			text_ul_tag = captiondiv.find_element_by_tag_name("ul")
#
#
#			# caption, tag, comment_num
#			li_tags = text_ul_tag.find_elements_by_tag_name("li")
#			commenter_user_is_owner = True
#			for li_tag in li_tags:
#				try:
#					text_board_a_tag = li_tag.find_element_by_tag_name("a")
#					if text_board_a_tag.get_attribute("title") == user['id'] and commenter_user_is_owner == True:
#						# li tag is a caption or tag
#						text_board_span_tag = li_tag.find_element_by_tag_name("span")
#						# print("Text: ", text_board_span_tag.get_attribute("innerHTML"))
#						caption += text_board_span_tag.text
#						# get tags
#						tags = text_board_span_tag.find_elements_by_tag_name("a")
#						for tag in tags:
#							# print("Tag: ", tag.text)
#							tag_list.append(tag.text)
#							try:
#								erase_pattern = re.compile(tag.text)
#								caption = re.sub(erase_pattern, '', caption)
#								#caption += ' '
#							except Exception as e:
#								print(e)
#
#
#					elif text_board_a_tag.get_attribute("title") != user['id']:
#						# li tag is a comment
#						# TODO: get all comments(if needed)
#						commenter_user_is_owner = False
#						comment_num += 1
#					else:
#						continue
#
#				except Exception as e: # Not possible
#					print("No <a> tag in this <li> tag")
#					print(e)
#
#			picture['caption'] = caption
#			picture['tag_list'] = tag_list
#			picture['num_of_comments'] = comment_num
#
#		except Exception as e:
#			print(e)
#			pass
#
