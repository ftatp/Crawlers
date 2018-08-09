import urllib.request
import urllib.parse
import requests

from urllib.request import urlopen, Request
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import json

import os
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

urls = [
	"https://www.instagram.com/mca4thfloor/",
	"https://www.instagram.com/sage.k_/"
]


login_url = "https://www.instagram.com/accounts/login/"
test_url = "https://www.instagram.com/mca4thfloor/"

phantomjs_path = "/home/ftatp/platform_tools/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
chrome_path = "/home/ftatp/platform_tools/chromedriver"
#browser = webdriver.PhantomJS(phantomjs_path)
browser = webdriver.Chrome(chrome_path)
browser.implicitly_wait(3)


USER = "ftatp5901@gmail.com"
PASS = "egoism1950"

session = requests.session()

login_info = {
	"m_id": USER,
	"m_passwd": PASS
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

for url in urls:
	browser.get(url)

	browser.save_screenshot("clickupdate.png")

	# get user's id
	# list of id contents
	# 1. profile
	# 2. number of followers
	# 3. number of followings

	user = {
		'id': "",
		'num_of_followers': 0,
		'num_of_followings': 0
	#	'picture_list": 
	}

	body = browser.find_element_by_tag_name("body")
	main = browser.find_element_by_tag_name("main")

	header = main.find_element_by_tag_name("header")

	nickname_tag = header.find_element_by_class_name("AC5d8")
	nickname = nickname_tag.get_attribute("innerHTML")
	user['id'] = nickname
	user_path = os.getcwd() + "/" + nickname

	if not os.path.isdir(user_path):#user 폴더가 존재 하지 않으면
		os.mkdir(user_path)

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
			user['num_of_followers'] = int(li_text_split[0])

		if li_text_split[1] == "following":
			user['num_of_following'] = int(li_text_split[0])
		
	print("User: ", user)


	# get picture panel
	browser.find_element_by_class_name("_2z6nI")

	picture_list = []

	picture_panel = main.find_element_by_class_name(" _2z6nI")
	i = 0

	img_divs = picture_panel.find_elements_by_class_name("eLAPa")

	for img_div in img_divs:
		i += 1
		if i > 50:
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
		#	'tag_list': [],
			'like_list': [],
			'num_of_like': 0,
			'num_of_comments': 0,
			'location': "",
			'date_time': ""
		}

		tag_list = []
		like_list = []
		comment_num = 0
		
		img_src_div = img_div.find_element_by_class_name("KL4Bh")
		img_tag = img_src_div.find_element_by_tag_name("img")

		img_link = img_tag.get_attribute("src")
		req = Request(url=img_link, headers=headers)
		img = urlopen(req).read()

		picture_path = user_path + "/picture" + str(i) + ".jpg"
		with open(picture_path, mode='wb') as f:
			f.write(img)
			picture['path'] = user['id'] + "/picture" + str(i) + ".jpg"
			print("Saved...")

		img_div.click()
		WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("M9sTE"))

		article_tag = browser.find_element_by_class_name("M9sTE")
		captiondiv = article_tag.find_element_by_class_name("eo2As")

		text_ul_tag = captiondiv.find_element_by_class_name("Xl2Pu")

		li_tags = text_ul_tag.find_elements_by_tag_name("li")
		for li_tag in li_tags:	
			tag_flag = False
			caption_flag = False
			try:
				text_board_a_tag = li_tag.find_element_by_tag_name("a")
				if text_board_a_tag.get_attribute("title") != user['id']:
					# li tag is a comment
					# TODO: get all comments(if needed)
					comment_num += 1
				elif caption_flag == False or tag_flag == False:
					# li tag is a caption or tag
					text_board_span_tag = li_tag.find_element_by_tag_name("span")
					print("Text: ", text_board_span_tag.get_attribute("innerHTML"))
					
					tags = text_board_span_tag.find_elements_by_tag_name("a")
					if len(tags) == 0:
						if caption_flag == False:
							#li tag is a the caption
							caption_flag = True
							picture['caption'] = text_board_span_tag.get_attribute("innerHTML")
					else:
						if tag_flag == False:
							tag_flag = True
							# li tag is the tag
							for tag in tags:
								tag_list.append(tag.get_attribute("innerHTML"))

			except: # Not possible
				print("No <a> tag in this <li> tag")
				pass

		picture['num_of_comments'] = comment_num
		picture['tag_list'] = tag_list
		# location
		try:
			ownerdiv = article_tag.find_element_by_class_name("Ppjfr")
			locationdiv = ownerdiv.find_element_by_class_name("M30cS")
			location_tag = locationdiv.find_element_by_class_name("O4GlU")
			picture['location'] = location_tag.text
		except:
			picture['location'] = ""


		# Date time
		time_tag = captiondiv.find_element_by_tag_name("time")
		date_time = time_tag.get_attribute("title")
		picture['date_time'] = date_time

		# Like list
		like_list = []	
		try:
			like_span_tag = captiondiv.find_element_by_class_name("zV_Nj")
			picture['num_of_like'] = int(like_span_tag.text.split(' ')[0])
			# click like button and get like user list
			like_span_tag.click()
			WebDriverWait(browser, timeout=500).until(lambda x: x.find_element_by_class_name("wwxN2"))

			like_users = find_elements_by_class_name("FPmhX")

			like_list = [ like_user.text for like_user in like_users ]

		except:
			print("Only view numbers")
		
		picture['like_list'] = like_list


		# data construction done
		print("Pic: ", picture)

		picture_list.append(picture)

		# click x span
		close_button = browser.find_element_by_class_name("ckWGn")
		close_button.click()

		# page down and repeat
		if img_div == img_divs[len(img_divs) - 1]:
			print("Scroll down\n\n")
			body.send_keys(Keys.PAGE_DOWN)
			time.sleep(1)
			new_img_divs = picture_panel.find_elements_by_class_name("eLAPa")

			idx = 0
			for new_img_div in new_img_divs:
				if new_img_div == img_div:
					break
				idx += 1

			img_divs += new_img_divs[idx + 1:]

		picture_list.append(picture)



	user['picture_list'] = picture_list

	print(user)

	# build json
	with open(user['id'] + "/data.json", 'w') as fp:
		json.dump(user, fp)




