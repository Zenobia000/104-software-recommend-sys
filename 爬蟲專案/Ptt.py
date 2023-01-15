from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json
import pandas as pd

# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")  # 最大化視窗
my_options.add_argument("--incognito")  # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  # 設定為正體中文


driver = webdriver.Chrome(
    options=my_options,
    service=Service(ChromeDriverManager().install())
)


# 去薪資工作版
driver.get('https://www.ptt.cc/bbs/Soft_Job/index.html')
# --------------------------------------------------------------------------
# 調整要爬的page範圍
large = int(input('請輸入起始頁數(例如3680)：'))
small = int(input('請輸入結束頁數(例如3675)：'))

print('=======================================')
print('起始頁:'+str(large))
print('結束頁:'+str(small))
print('=======================================')
# 你要放哪裡
folderPath = 'C:/Users/student/python_web_scraping-master/ptt/'
#爬幾個連結的檔名 (應該可以改成一個input輸入)
filename_innerText = 'page_'+str(large)+'_'+str(small)
# --------------------------------------------------------------------------

results = []
alinks = []
atitle = []
alinks = []
atitle = []
result1 = []
all_acc = []
all_date = []
all_pop_num = []


def links():
    links = driver.find_elements(By.CSS_SELECTOR, '  div.title > a')

    post_accs = driver.find_elements(By.CSS_SELECTOR, 'div.meta > div.author')
    for post_acc in post_accs:
        acc = post_acc.get_attribute('innerText')
        all_acc.append(acc)

    post_dates = driver.find_elements(By.CSS_SELECTOR, 'div.meta > div.date')
    for post_date in post_dates:
        date = post_date.get_attribute('innerText')
        all_date.append(date)

    pops = driver.find_elements(By.CSS_SELECTOR, 'div.nrec')
    for pop in pops:
        pop_num = pop.get_attribute('innerText')
        if pop_num == '':
            pop_num = pop_num+'None'
        all_pop_num.append(pop_num)

    for i in range(len(links)):
        plink = links[i].get_attribute('href')
        ptitle = links[i].get_attribute('innerText')
        alinks.append(plink)
        atitle.append(ptitle)
        rr = {
            '發文帳號': all_acc[i],
            ptitle: plink,
            '發文時間': all_date[i],
            '回應數量': all_pop_num[i]
        }
        results.append(rr)


def reply(j):
    driver.get(alinks[j])
    innerTexts = driver.find_elements(By.CSS_SELECTOR, 'div.push')
    oUser = ''
    for innerText in innerTexts:
        comment = innerText.get_attribute('innerText')
        c = comment.split('\n')
        fc = c[0].split(':')
        fc[-1]

        cc = comment.split(' ')
        GB = cc[0]
        try:
            User = cc[1]
        except:
            print('抓不到')
        innertext = fc[-1]
        try:
            if oUser == User:
                text = result1[-1]['留言內文']
                text += innertext
                result1[-1]['留言內文'] = text
            else:
                oUser = User
                result = {
                    '留言好壞': GB,
                    '留言帳號': User,
                    '留言內文': innertext

                }
                result1.append(result)
        except:
            print('沒有評論')


def savejson():
    with open(f'{folderPath}{filename_innerText}'+'.json', "a", encoding='utf-8') as file:
        file.write(json.dumps(
            results, ensure_ascii=False, indent=4))
    print("檔案", filename_innerText, "存好了")

    df = pd.read_json(f'{folderPath}{filename_innerText}'+'.json')
    df.to_csv(f'{folderPath}{filename_innerText}'+'.csv',
              index=None, encoding="utf_8_sig")


if __name__ == '__main__':
    driver.get('https://www.ptt.cc/bbs/Soft_Job/index'+str(large)+'.html')
    for x in range(large, small, -1):
        driver.find_element(
            By.CSS_SELECTOR, '#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(2)').click()
        links()
    sleep(0.5)

    for i in range(len(alinks)):
        page = large - i//20
        num = i % 20
        print('目前第'+str(page)+'頁的第'+str(num)+'筆')
        result1 = []
        reply(i)
        results[i]['留言'] = result1
        sleep(0.5)
    savejson()


print(filename_innerText + '存好了')
driver.quit()
