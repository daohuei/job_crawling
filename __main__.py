from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import json
import requests

def get_job_info(job_soup, select_path_dict):
	# for Yourator:
	# Job Title: h1.flex-item > span:nth-of-type(1)
	# Job Description: section:nth-of-type(1).content__area 
	# Job Requirement: section:nth-of-type(2).content__area 

	job_info = {}

	job_info["job_title"] = job_soup.select(select_path_dict["job_title"]).text
	job_info["job_descript"] = job_soup.select(select_path_dict["job_descript"]).text
	job_info["job_require"] = job_soup.select(select_path_dict["job_require"]).text

	return job_info

def get_job_url_list(url_list_loc):
	# read text as list(url list)
	with open("./url_list.txt") as url_list_file:
		url_list = url_list_file.readlines()
	return url_list

def get_path():
	

if __name__ == '__main__':

	# website of job description
	url_list = get_job_url_list("./url_list.txt")

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
		print(job_url)
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
			sys.exit("Request Error: "+ str(requests.codes.ok))

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
	# Extract the job info and append them into info list
	info_list = []
	for job_info_soup in soup_list:
		info_list.append(get_job_info(job_info_soup))

	""" need encoding
	job_info_json = json.dumps(job_info)
	with open('job.json', 'w') as fp:
		fp.write(job_info_json)
	"""

	# write to csv file
	with open('job.csv', 'w', newline='') as csvfile:
		# 建立 CSV 檔寫入器
		writer = csv.writer(csvfile)
		header = info_list[0].keys()
		# 寫入header資料
		writer.writerow(header)
		for job_info in info_list:
			row = []
			for key in header:
				row.append(job_info[key])
			# 寫入content
			writer.writerow(row)

	print("scraping done.")

