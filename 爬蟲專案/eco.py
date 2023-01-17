from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import json
import pandas as pd

urlindex = input('請輸入網址編號 0~6:')

my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")  # 最大化視窗
my_options.add_argument("--incognito")  # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  # 設定為正體中文
my_options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖
my_options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])  # 沒有異常log
driver = webdriver.Chrome(
    options=my_options,
    service=Service(ChromeDriverManager().install()))

links = ['https://money.udn.com/money/cate/12017?from=edn_navibar',
         'https://money.udn.com/money/cate/11111?from=edn_navibar',
         'https://money.udn.com/money/cate/5592?from=edn_navibar',
]

url = links[int(urlindex)]
driver.get(url)

alinks = []
results = []

def input_links():
    links=driver.find_elements(By.CSS_SELECTOR,'section> ul > li > a')
    for i in links:
        urll=i.get_attribute('href')
        alinks.append(urll)
    print(len(alinks))
def more_links():
    more= driver.find_elements(By.CSS_SELECTOR,'section > div > span.more')
    for ii in range(len(more)):
        for jj in range (100):
            try:
                more[ii].click()
                sleep(0.5)
            except:
                continue
def crawler ():
    try:
        in_text = driver.find_element(
            By.CSS_SELECTOR, '#article_body')
        in_text = in_text.get_attribute('innerText')
        text = in_text.replace('\n', ' ')
    except:
        text = 'None'
    result = {
        '文章內容': text
    }
    results.append(result)


if __name__ == '__main__':
    more_links()
    input_links()
    for j in range(len(alinks)):
        print(j, alinks[j])
        driver.get(alinks[j])
        sleep(2)
        crawler()