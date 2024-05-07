import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()


def get_pacakge_screenshot(url_to_screenshot, url_type, package_type, package_name, output_folder):
    driver.get(url_to_screenshot)
    if 'Some information is still being processed' in driver.page_source:
        # todo: create files with failed screens
        return False

    screenshot_file_path = output_folder + "\\" + url_type + "_" + package_type + "_" + package_name + ".png"
    driver.save_screenshot(screenshot_file_path)
    return True
