from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect
from selenium.webdriver.common.action_chains import ActionChains
from io import BytesIO
import re
import base64
from PIL import Image
from PIL import ImageChops
from numpy import array
import numpy as np
import easing

# 避免网站认出这是selenium在模拟浏览器操作,window.navigator.webdriver = false
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_argument("--headless")

browser = webdriver.Chrome(service=Service(executable_path="./drivers/chromedriver.exe"), options=options)
browser.get('https://www.darty.com/nav/achat/gros_electromenager/index.html')
Wait(browser, 60).until(
    Expect.presence_of_element_located((By.TAG_NAME, "iframe"))
)
iframe = browser.find_element(By.TAG_NAME, "iframe")
browser.switch_to.frame(iframe)
Wait(browser, 60).until(
    Expect.presence_of_element_located((By.CSS_SELECTOR, '.geetest_radar_tip'))
)
browser.find_element(By.CSS_SELECTOR, '.geetest_radar_tip').click()

# print("yesetgsfdsdf")
# 获取拼图的缺陷背景bg,完整背景full_bg,碎片slice
Wait(browser, 60).until(
    Expect.presence_of_element_located((By.CSS_SELECTOR, '.geetest_canvas_bg'))
)

def canvas_to_base64(css_selector):
    canvas = browser.find_element(By.CSS_SELECTOR, css_selector)
    return browser.execute_script("return arguments[0].toDataURL()", canvas)
# bg = browser.find_element(By.CSS_SELECTOR, '.geetest_canvas_bg')
bg_base64 = canvas_to_base64(".geetest_canvas_bg")
# full_bg = browser.find_element(By.CSS_SELECTOR, '.geetest_canvas_fullbg')
full_bg_base64 = canvas_to_base64(".geetest_canvas_fullbg")
# slice = browser.find_element(By.CSS_SELECTOR, '.geetest_canvas_slice')
slice_base64 = canvas_to_base64(".geetest_canvas_slice")

def base64_to_img(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    image = base64.b64decode(base64_data)
    image_data = BytesIO(image)
    return Image.open(image_data).convert('RGB')

im_bg = base64_to_img(bg_base64)
im_full_bg = base64_to_img(full_bg_base64)

def get_offset(diff):
    im = array(diff)
    width, height = diff.size
    print(width, height)
    diff = []
    for i in range(height):
        for j in range(width):
            if im[i, j, 0] > 50 or im[i, j, 1] > 50:
                diff.append(j)
                break
    return min(diff)

diff = ImageChops.difference(im_bg, im_full_bg)
offset = get_offset(diff) - 6
print(offset)
Wait(browser, 60).until(
    Expect.presence_of_element_located((By.CSS_SELECTOR, '.geetest_slider_button'))
)


def fake_drag(knob, offset):
    offsets, tracks = easing.get_tracks(offset, 1.656, 'ease_out_expo')
    ActionChains(browser).click_and_hold(knob).perform()
    for x in tracks:
        print(x)
        ActionChains(browser).move_by_offset(x, 0).perform()
    ActionChains(browser).pause(0.056).release().perform()
    return



knob = browser.find_element(By.CSS_SELECTOR, '.geetest_slider_button')
fake_drag(knob, offset)
browser.switch_to.default_content()

Wait(browser, 60).until(
    Expect.visibility_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
)
accept = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
accept.click()

Wait(browser, 60).until(
    Expect.presence_of_element_located((By.CSS_SELECTOR, '#main-tab'))
)
a = browser.find_element(By.CSS_SELECTOR, '#main-tab > ul > li:first-child > ul > li:first-child > ul > li:first-child > a')
print(a.get_attribute("href"), '下一级路径')
a.click()
# browser.get(a.get_attribute("href"))
# print(a.get_attribute("href"))
# a.click()

# def drag_and_drop(offset):
#     ActionChains(browser).drag_and_drop_by_offset(knob, offset, 0).perform()

# drag_and_drop(offset)









# def get_slider_offset():


