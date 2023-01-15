from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
import subprocess

import pandas as pd


with open('job7_all.json', 'r', encoding='utf-8') as infile:
    jobsjson = json.load(infile)
    
jobscsv = pd.read_csv('job5_all_v2.csv', encoding='utf-8-sig')


my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")         #最大化視窗
my_options.add_argument("--incognito")               #開啟無痕模式
my_options.add_argument("--disable-popup-blocking") #禁用彈出攔截
my_options.add_argument("--disable-notifications")  #取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  #設定為正體中文

driver = webdriver.Chrome(
    options = my_options,
    service = Service(ChromeDriverManager().install())
)


for i in range(len(jobscsv)):
    needp_b = jobscsv.loc[i, '需求人數']
    if needp_b == '不限' or needp_b == '一個月內' or needp_b == '兩週內' or needp_b == '一週內': #可上班日
        driver.get(jobscsv.loc[i, '職缺連結'])
        sleep(1)
        print(i, jobscsv.loc[i, '職缺連結'], end=' ')
        try:
            IDN = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                    'div.job-header__btn.mb-3 > div > form > input[type=hidden]:nth-child(1)')
                )
            )
        except TimeoutException:
            print('職缺已下架')
            continue
            
        try:
            needp = driver.find_element(
                    By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(12) > div.col.p-0.list-row__data > div').get_attribute("innerText")
        except:
            try:
                needp = driver.find_element(
                        By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(11) > div.col.p-0.list-row__data > div').get_attribute("innerText")
            except:
                try:
                    needp = driver.find_element(
                            By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(10) > div.col.p-0.list-row__data > div').get_attribute("innerText")
                except:
                    needp = driver.find_element(
                            By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(9) > div.col.p-0.list-row__data > div').get_attribute("innerText")                   
        print(needp_b, needp)
        jobscsv.loc[i, '需求人數'] = needp
        jobsjson[i]['需求人數'] = needp
        
    elif needp_b == '週休二日' or needp_b == '依公司規定': #休假制度
        driver.get(jobscsv.loc[i, '職缺連結'])
        sleep(1)
        print(i, jobscsv.loc[i, '職缺連結'], end=' ')
        try:
            IDN = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                    'div.job-header__btn.mb-3 > div > form > input[type=hidden]:nth-child(1)')
                )
            )
        except TimeoutException:
            print('職缺已下架')
            continue
            
        try:
            needp = driver.find_element(
                    By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(14) > div.col.p-0.list-row__data > div').get_attribute("innerText")
        except:
            try:
                needp = driver.find_element(
                        By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(11) > div.col.p-0.list-row__data > div').get_attribute("innerText")
            except:
                needp = driver.find_element(
                        By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(10) > div.col.p-0.list-row__data > div').get_attribute("innerText")
                
        print(needp_b, needp)
        jobscsv.loc[i, '需求人數'] = needp
        jobsjson[i]['需求人數'] = needp


driver.quit()


with open('job5_all_v2.json', "w", encoding='utf-8') as file:
    file.write(json.dumps(jobsjson, ensure_ascii=False, indent=4))
print("json檔更新完畢")

jobscsv.to_csv('job5_all_v3.csv',index=None, encoding="utf_8_sig")
print("csv檔更新完畢")