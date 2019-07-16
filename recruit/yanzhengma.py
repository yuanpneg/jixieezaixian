import time
import random
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying_Client

EMAIL = '******************'
PASSWORD = '**********************'

CHAOJIYING_USERNAME = '********'
CHAOJIYING_PASSWORD = '*********'
CHAOJIYING_SOFT_ID = '**************'
CHAOJIYING_KIND = 9004


class CrackTouClick():
    def __init__(self):
        self.url_one = 'https://www.tianyancha.com/'
        # self.url_two = 'https://www.tianyancha.com/search?key=郑州宇通集团有限公司'
        self.url_two = 'https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fcompany%2F3105819146&rnd='
        self.browser = webdriver.Chrome(r"D:\chromedriver.exe")
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
        self.sleep_time = random.uniform(1, 2)
        self.cookie_one = {
            'domain': '.tianyancha.com',
            "name": "tyc-user-info",
            "value": "=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E4%25BB%25BB%25E7%259B%2588%25E7%259B%2588%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%252228%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODczOTEzODc4MiIsImlhdCI6MTU0Njk5NTYwMiwiZXhwIjoxNTYyNTQ3NjAyfQ.BEouV6Vs2qq1hehuxwuXXYcmQO9C2BZa1GMfVEYIhQasu8mMwr3IqxE_bzK2ENU0OGltFK3X8dBkBxxW4IzzqQ%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218739138782%2522%257D"
        }
        self.cookie_two = {
            'domain': '.tianyancha.com',
            "name": "auth_token",
            "value": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODczOTEzODc4MiIsImlhdCI6MTU0Njk5NTYwMiwiZXhwIjoxNTYyNTQ3NjAyfQ.BEouV6Vs2qq1hehuxwuXXYcmQO9C2BZa1GMfVEYIhQasu8mMwr3IqxE_bzK2ENU0OGltFK3X8dBkBxxW4IzzqQ"
        }
        self.suijishu = random.uniform(1,2)

    def open(self):  # 打开网页输入用户名密码
        self.browser.get(self.url_one)
        time.sleep(self.sleep_time)
        self.browser.add_cookie(self.cookie_one)
        self.browser.add_cookie(self.cookie_two)
        self.browser.get(self.url_two)

    def get_touclick_button(self):  # 获取初始验证按钮element_to_be_clickable
        button = self.wait.until(EC.presence_of_element_located((By.ID, 'refeshie')))
        return button

    def get_touclick_element(self):  # 获取验证图片对象
        element = self.wait.until(EC.presence_of_element_located((By.ID, 'bgImgie')))
        return element

    def get_position(self):  # 获取验证码位置
        element = self.wait.until(EC.presence_of_element_located((By.ID, 'targetImgie')))
        time.sleep(2)
        location = element.location
        size = element.size
        top = location['y']
        bottom = location['y'] + 140
        left = location['x']
        right = location['x'] + size['width']
        return (left, top, right, bottom)

    def get_screenshot(self):  # 获取网页截图
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_image(self, name='captcha.png'):  # 获取验证码图片
        left, top, right, bottom = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_points(self, captcha_result):  # 解析识别结果
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):  # 点击验证图片
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0],
                                                                   location[1] - 40).click().perform()
            time.sleep(random.uniform(1,2))

    def touch_click_verify(self):  # 点击验证按钮
        button = self.wait.until(EC.presence_of_element_located((By.ID, 'submitie')),1000)
        button.click()

    def crack(self):  # 破解入口
        self.open()
        time.sleep(2)
        # 点击验证按钮
        button = self.get_touclick_button()
        button.click()
        time.sleep(2)
        # 获取验证码图片
        image = self.get_touclick_image("tyc.png")
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码mysqld.exe -install
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        time.sleep(2)
        # 判定是否成功
        elem = self.wait.until(
            # EC.text_to_be_present_in_element((By.CLASS_NAME, 'touclick-hod-note'), '验证成功'))
            EC.presence_of_element_located((By.ID, 'refeshie')),300)
        # 失败后重试
        print(elem.text)
        if len(elem.text) == 0:
            self.browser.quit()
        else:
            print('fail!')
            self.crack()