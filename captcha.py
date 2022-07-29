from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect

# 避免网站认出这是selenium在模拟浏览器操作,window.navigator.webdriver = false
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

browser = webdriver.Chrome(service=Service(executable_path="./drivers/chromedriver.exe"), options=options)
browser.get('https://www.darty.com/nav/achat/gros_electromenager/index.html')
Wait(browser, 60).until(
    Expect.visibility_of_element_located((By.TAG_NAME, "iframe"))
)
iframe = browser.find_element(By.TAG_NAME, "iframe")
browser.switch_to.frame(iframe)
Wait(browser, 60).until(
    Expect.visibility_of_element_located((By.CSS_SELECTOR, '.geetest_radar_tip'))
)
browser.find_element(By.CSS_SELECTOR, '.geetest_radar_tip').click()

# 获取拼图的缺陷背景bg,完整背景full_bg,碎片slice
Wait(browser, 60).until(
    Expect.visibility_of_element_located((By.CSS_SELECTOR, '.geetest_canvas_bg'))
)
bg = browser.find_element(By.CSS_SELECTOR, '.geetest_canvas_bg')
bg_base64 = browser.execute_script("return arguments[0].toDataURL()", bg)
print(bg_base64)
full_bg = browser.find_element(By.CSS_SELECTOR, '.geetest_canvas_fullbg')
full_bg_base64 = browser.execute_script("return arguments[0].toDataURL()", full_bg)
slice = browser.find_element(By.CSS_SELECTOR, '.geetest_canvas_slice')
slice_base64 = browser.execute_script("return arguments[0].toDataURL()", slice)

