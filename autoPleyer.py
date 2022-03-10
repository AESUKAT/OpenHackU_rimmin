import time
from selenium import webdriver
import os.path
def call_selenium(target_url, best_moments):
    user_name = os.path.expanduser('~').split("\\")[-1]
    profilefolder = '--user-data-dir=' + rf"C:\Users\{user_name}\AppData\Local\Google\Chrome\User Data"
    options = webdriver.ChromeOptions()
    options.add_argument(profilefolder)

    driver = webdriver.Chrome(
        executable_path = r"./chromedriver.exe",
        options = options
    )

    for i in range(len(best_moments)):
        target_section_start = target_url + "&t=" + str(best_moments[i][0]) + "s"
        driver.get(target_section_start)
        print(best_moments[i][1] - best_moments[i][0])
        time.sleep(best_moments[i][1] - best_moments[i][0])

    driver.quit()

def main():
    target_url = "https://www.youtube.com/watch?v=nBZTIJHZZm0"
    best_moments = [[305,335], [1478,1508], [373,403]]
    call_selenium(target_url, best_moments)

if __name__=="__main__":
    main()