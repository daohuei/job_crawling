from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import sys
import time
import os
import csv

def get_job_list(page_soup):
	# Yourator Job Search
	# job_title: .y-card-content-title > a
	# job_link: .y-card-content-title > a
	# company: .y-card-content-subtitle > a
	# company_link: .y-card-content-subtitle > a

	job_list = []

	job_soup_list = page_soup.select(".y-card-content")

	for js in job_soup_list:
		# select the title and company <a> tag section
		title = js.select(".y-card-content-title > a")[0]
		company = js.select(".y-card-content-subtitle > a")[0]

		# store the info with job_ele dictionary
		job_ele = {}
		job_ele["job_title"] = title.text
		job_ele["job_link"] = "https://www.yourator.co"+title.get('href')
		job_ele["company"] = company.text
		job_ele["company_link"] = "https://www.yourator.co"+company.get('href')
		job_list.append(job_ele)

	return job_list

def write_csv(j_list):
	header = []
	needHeader = False
	# 檢查檔案是否存在
	if not os.path.isfile("job_search.csv"):
		needHeader = True
	else:
		with open('job_search.csv', "r") as f:
			reader = csv.reader(f)
			header = next(reader, None)
			print(header)
	# write to csv file
	with open('job_search.csv', 'a', newline='') as csvfile:
		if needHeader:
			header = j_list[0].keys()

		# 將 dictionary 寫入 CSV 檔
		writer = csv.DictWriter(csvfile, fieldnames=header)
		# 檢查檔案是否存在
		if needHeader:
			# 寫入第一列的欄位名稱
			writer.writeheader()

		for j in j_list:
			# 寫入content
			writer.writerow(j)

def main():
	# setup Chrome option
	options = webdriver.ChromeOptions()
	# maximize windows
	# options.add_argument("--start-maximized")
	# private mode
	options.add_argument("--incognito")
	# invisible
	options.add_argument("--headless")
	print('Opening Browser...')
	# adapt the option
	browser = webdriver.Chrome(chrome_options=options,
							   executable_path='./chromedriver')

	# Get all the job in certain search
	job_url = "https://www.yourator.co/jobs?category[]=29&tag[]=135"

	
	pages = [1,2,3,4,5]
	for i in pages:
		print(i)
		browser.get(job_url+"&page="+str(i))
		time.sleep(1)
		page_soup = BeautifulSoup(browser.page_source, 'html.parser')
		j_list = get_job_list(page_soup)
		if len(j_list) == 0:
			break
		write_csv(j_list)

	# quit the browser
	browser.quit()
	

	"""
	# GET method
	req = requests.get(job_url)
	j_list = []
	# print out the status code
	if req.status_code == requests.codes.ok:
		print("OK:", requests.codes.ok)
		# print(req.text)
		# scrape the website content
		page_soup = BeautifulSoup(req.text, 'html.parser')
		j_list = get_job_list(page_soup)

	else:
		sys.exit("Request Error: "+ str(req.status_code))
	"""



if __name__ == '__main__':
	main()
	print("Scraping Done")
