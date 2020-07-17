import csv
import os

path_dict = {}
path_dict["job_hunt_website"] = input("Input the name of Job Hunt Website: ")
path_dict["job_title"] = input("Input the path of Job Title: ")
path_dict["job_descript"] = input("Input the path of Job Description: ")
path_dict["job_require"] = input("Input the path of Job Requirement: ")

needHeader = False
# 檢查檔案是否存在
if not os.path.isfile("path.csv"):
	needHeader = True

# write to csv file
with open('path.csv', 'a', newline='') as csvfile:

	header = ["job_hunt_website", "job_title", "job_descript", "job_require"]
	# 將 dictionary 寫入 CSV 檔
	writer = csv.DictWriter(csvfile, fieldnames=header)
	if needHeader:
		# 寫入第一列的欄位名稱
		writer.writeheader()

	# 寫入content
	writer.writerow(path_dict)