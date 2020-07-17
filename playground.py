from selenium import webdriver
import time
import requests

# GET method
req = requests.get("https://www.yourator.co/companies/Vizuro/jobs/12347")
# print out the status code
if req.status_code == requests.codes.ok:
	print("OK:", requests.codes.ok)
	print(req.text)

# 100 - 199 : Info response
# 200 - 299 : Success response
# 300 - 399 : redirect
# 400 - 499 : client err
# 500 - 599 : server err


""" Multiple windows browser activator
count = 0
wincount=0
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
print('Opening Browser...')
browser = webdriver.Chrome(chrome_options=options,
                           executable_path='./chromedriver')
#browser.switch_to.window(browser.window_handles[0])
for n in range (77):
	browser.execute_script("window.open()")
	browser.get("http://127.0.0.1")
	time.sleep(1)
	print('crawl')
	count += 1
	wincount += 1
	print(count)
	if wincount == 4:
		for k in range(4):
			browser.switch_to.window(browser.window_handles[0])
			browser.close()
			browser.switch_to.window(browser.window_handles[0])
		wincount = 0

print(count)
"""
""" read json
with open('./job_descript.txt') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(data)
"""
"""
# read text as list(url list)
with open("./url_list.txt") as url_list_file:
	line = url_list_file.readlines()
	print(len(line))
	for u in line:
		print(u.strip())
"""		

