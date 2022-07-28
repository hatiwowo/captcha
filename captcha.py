from cv2 import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect

browser = webdriver.Chrome(service=Service(executable_path="./drivers/chromedriver.exe"))
browser.get('https://www.darty.com/nav/achat/gros_electromenager/index.html')
iframe = browser.find_element(By.TAG_NAME, "iframe")
browser.switch_to.frame(iframe)
browser.find_element(By.CSS_SELECTOR, '.geetest_radar_tip').click()