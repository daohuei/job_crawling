from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import sys
import json
import requests

def get_job_info(job_soup, select_path_dict):
	# for Yourator:
	# Job Title: h1.flex-item > span:nth-of-type(1)
	# Job Description: .job__content > section:nth-of-type(1)
	# Job Requirement: .job__content > section:nth-of-type(2) 

	job_info = {}

	job_info["job_title"] = job_soup.select(select_path_dict["job_title"])[0].text
	job_info["job_descript"] = job_soup.select(select_path_dict["job_descript"])[0].text
	job_info["job_require"] = job_soup.select(select_path_dict["job_require"])[0].text


	return job_info

def get_job_url_list(url_list_loc):
	url_list = []
	# read text as list(url list)
	with open(url_list_loc) as csvfile:
		csv_dict = csv.DictReader(csvfile)
		for row in csv_dict:
			url_list.append(row['job_link'])
	return url_list

def get_path(pathfile):
	with open(pathfile, newline='') as csvfile:
		dict_list = []
		# 讀取 CSV 檔內容，將每一列轉成一個 dictionary
		csv_dict = csv.DictReader(csvfile)
		for row in csv_dict:
			dict_list.append(row)

	return dict_list



if __name__ == '__main__':

	# website of job description
	url_list = get_job_url_list("job_search.csv")

	"""
	# setup Chrome option
	options = webdriver.ChromeOptions()
	# maximize windows
	options.add_argument("--start-maximized")
	# private mode
	options.add_argument("--incognito")
	# invisible
	# options.add_argument("--headless")
	print('Opening Browser...')
	# adapt the option
	browser = webdriver.Chrome(chrome_options=options,
							   executable_path='./chromedriver')
	"""
	
	# Simply using python request
	soup_list = []
	for job_url in url_list:

		# GET method
		req = requests.get(job_url)
		# print out the status code
		if req.status_code == requests.codes.ok:
			print("OK:", requests.codes.ok)
			# print(req.text)
			# scrape the website content
			soup = BeautifulSoup(req.text, 'html.parser')
			soup_list.append(soup)
		else:
			sys.exit("Request Error: "+ str(req.status_code))

	"""	Multiple Chrome Window Activator(Not Completed)
	wincount = 0
	soup_list = []
	for job_url in url_list:
		browser.execute_script("window.open()")
		# go to the website
		browser.get(job_url.strip())
		wincount += 1
		if wincount == 4 or wincount == len(url_list):
			for k in range(wincount):
				browser.switch_to.window(browser.window_handles[0])
				# scrape the website content
				#soup = BeautifulSoup(browser.page_source, 'html.parser')
				#soup_list.append(soup)
				browser.close()
				browser.switch_to.window(browser.window_handles[0])
			wincount = 0
		
		# quit the browser
		browser.quit()
	"""

	selector_path_list = get_path("path.csv")
	# Extract the job info and append them into info list
	info_list = []
	for job_info_soup in soup_list:
		info_list.append(get_job_info(job_info_soup,selector_path_list[0]))

	""" need encoding
	job_info_json = json.dumps(job_info)
	with open('job.json', 'w') as fp:
		fp.write(job_info_json)
	"""

	needHeader = False
	# 檢查檔案是否存在
	if not os.path.isfile("job.csv"):
		needHeader = True
	# write to csv file
	with open('job.csv', 'a', newline='') as csvfile:

		header = info_list[0].keys()
		# 將 dictionary 寫入 CSV 檔
		writer = csv.DictWriter(csvfile, fieldnames=header)

		# 檢查檔案是否存在
		if needHeader:
			# 寫入第一列的欄位名稱
			writer.writeheader()

		for job_info in info_list:
			# 寫入content
			writer.writerow(job_info)

	print("scraping done.")

