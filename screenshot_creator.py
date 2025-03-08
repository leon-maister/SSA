import os.path
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_driver_path = ChromeDriverManager().install()
chrome_driver_path = os.path.join(os.path.dirname(chrome_driver_path), 'chromedriver.exe')
print(chrome_driver_path)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()


def get_pacakge_screenshot(url_to_screenshot, url_type, package_type, package_name, output_folder):
    driver.get(url_to_screenshot)
    if 'Some information is still being processed' in driver.page_source:
        time.sleep(15)
        driver.refresh()


    # if 'Project Not found' in driver.page_source:
    #     # todo: create files with failed screens
    #     return False

    screenshot_file_path = output_folder + "\\" + url_type + "_" + package_type + "_" + package_name + ".png"
    driver.save_screenshot(screenshot_file_path)
    return True
