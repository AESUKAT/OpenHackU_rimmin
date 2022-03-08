import time
from selenium import webdriver
import csv

target_url = "https://www.youtube.com/watch?v=nBZTIJHZZm0"

best_moments = []
with open('moment.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        rowlist = [row]
        best_moments += rowlist
profilefolder = '--user-data-dir=' + r"C:\Users\admin\AppData\Local\Google\Chrome\User Data"

options = webdriver.ChromeOptions()
options.add_argument(profilefolder)

driver = webdriver.Chrome(
    executable_path = r"./chromedriver.exe",
    options = options
)

for i in range(len(best_moments)):
    target_section_start = target_url + "&t=" + best_moments[i][0] + "s"
    driver.get(target_section_start)

    '''
    print(best_moments[i][0], best_moments[i][1])
    print(target_section_start)
    '''

    time.sleep(int(best_moments[i][1]) - int(best_moments[i][0]))

driver.quit()