from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sys
import csv


def browser_setup():
	# setup Chrome option
	options = webdriver.ChromeOptions()
	# maximize windows
	# options.add_argument("--start-maximized")
	# private mode
	options.add_argument("--incognito")
	# invisible
	options.add_argument("--headless")
	return options

def get_job_list(page_soup):
	# 104 Job Search
	# job_title: article.job-list-item a.js-job-link
	# job_link: article.job-list-item a.js-job-link
	# company: article.job-list-item  ul:nth-of-type(1) a
	# company_link: article.job-list-item  ul:nth-of-type(1) a

	job_list = []

	job_soup_list = page_soup.select("article.job-list-item")

	for js in job_soup_list:
		if "js-job-item--recommend" in str(js) or "b-block--nodata" in str(js):
			break
		# select the title and company <a> tag section
		title = js.select("a.js-job-link")[0]
		company = js.select("ul:nth-of-type(1) a")[0]
		# store the info with job_ele dictionary
		job_ele = {}
		job_ele["job_title"] = title.text.replace('"',"").strip()
		job_ele["job_link"] = "https:"+title.get('href')
		job_ele["company"] = company.text.replace('"',"").strip()
		job_ele["company_link"] = "https:"+company.get('href')
		job_list.append(job_ele)

	return job_list

def get_104_content():
	pass

def search_104(url_list, fn):
	options = browser_setup()
	print('Opening Browser...')
	# adapt the option
	browser = webdriver.Chrome(chrome_options=options,
							   executable_path='./chromedriver')
	for url in url_list:
		browser.get(url)
		"""
		# Scroll down to bottom, move to next page in 104
		for i in range(3):
			# execute the js script with browser driver
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
		"""
		job_soup = BeautifulSoup(browser.page_source, 'html.parser')
		job_list = get_job_list(job_soup)
		write_csv(job_list, fn)
	browser.quit()

def write_csv(j_list, filename):
	print(len(j_list))
	header = []
	needHeader = False
	# 檢查檔案是否存在
	if not os.path.isfile(filename):
		needHeader = True
	else:
		with open(filename, "r") as f:
			reader = csv.reader(f)
			header = next(reader, None)
			print(header)
	# write to csv file
	with open(filename, 'a', newline='') as csvfile:
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
	""" # full-time + intern maybe
	url_list = [
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=%E5%BE%8C%E7%AB%AFAI&jobcatExpansionType=0&area=6001001000&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=人工智慧&jobcatExpansionType=0&area=6001001000&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=machine%20learning&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=ai%20%E5%B7%A5%E7%A8%8B%E5%B8%AB&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=deep%20learning&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=深度學習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=資料科學&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=自然語言&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=大數據&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=資料分析&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=資料工程&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=NLP&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
	]
	search_104(url_list, "job_search_104.csv")
	""" 
	# focus on internship
	url_list_intern = [
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=%E5%BE%8C%E7%AB%AFAI實習&jobcatExpansionType=0&area=6001001000&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=人工智慧實習&jobcatExpansionType=0&area=6001001000&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=machine%20learning實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=ai%20%E5%B7%A5%E7%A8%8B%E5%B8%AB實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=deep%20learning實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=深度學習實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=資料科學實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=自然語言實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=大數據實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=資料分析實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=資料工程實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
		"https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001004%2C2007001006%2C2007001012%2C2007001007&keyword=NLP實習&jobcatExpansionType=0&area=6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc",
	]
	search_104(url_list_intern, "job_search_104_intern.csv")

if __name__ == '__main__':
	main()