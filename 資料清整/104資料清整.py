import re
import numpy as np
import pandas as pd
import collections

import json

from pprint import pprint

jobs = pd.read_csv('job5_all_v2.csv', encoding='utf-8-sig')


#到其他條件前有30欄 再扣除工作內容
jobs = jobs.dropna(thresh=29).reset_index(drop=True)
print(jobs.isnull().sum())

# 工作性質只留全職
jobs = jobs.drop(jobs[jobs['工作性質'] != '全職'].index).reset_index(drop=True)
print(collections.Counter(jobs['工作性質']))

# drop 欄位歪掉
problem_id1 = []
for i in range(len(jobs)):
    salary = jobs.loc[i, "工作待遇"]
    if salary == None or (salary[:2] != '年薪' and salary[:2] != '月薪' and salary[:2] != '日薪' and salary[:2] != '時薪'\
                     and salary[:4] != '待遇面議' and salary[:4] != '論件計酬'):
        problem_id1.append(i)
jobs = jobs.drop(problem_id1).reset_index(drop=True)

problem_id2 = []
for i in range(len(jobs)):
    manage = jobs.loc[i, "管理責任"]
    if manage == None or (manage != '不需負擔管理責任' and manage != '管理人數未定' and manage != '管理4人以下' and \
                         manage != '管理5-8人' and manage != '管理9-12人' and manage != '管理13人以上'):
        problem_id2.append(i)
jobs = jobs.drop(problem_id2).reset_index(drop=True)

# 清整資料


# 需要增加的空欄位
jobs['工作待遇_min'] = None
jobs['工作待遇_max'] = None
jobs['年齡分佈_小於30'] = None
jobs['年齡分佈_大於30'] = None

r_d = r'\d{1,3}[,\d{3}]*'
r_d2 = r'\d+'

r_day = r'日'
r_night = r'輪|晚|夜'

regex01 = r'\d+億\d+萬' #有億有萬
regex02 = r'\d+億|\d+萬' #只有億或只有萬

re_otherword = r"、"
re_chinese = r"贊助提升專業能力"
re_space_one = r'\s'
re_space_ones = r'\s+'

r_emp = r'\d+'
r_tag = r'(?<=上市櫃)|(?<=外商)|(?<=科)|(?<=其他)'


def convert_num(str_d):
    return int(str_d.replace(",", ""))

# %%
for i in range(len(jobs)):
    
    # 職缺名稱
    jobname = jobs.loc[i, '職缺名稱'].split()
    jobs.loc[i, '職缺名稱'] = ' '.join(jobname[:-1])
    
    # 工作待遇
    salary = jobs.loc[i, '工作待遇']
    if salary != None:
        s_str = re.findall(r_d, salary)
        if salary == '待遇面議（經常性薪資達 4 萬元或以上）': 
            jobs.loc[i, '工作待遇_min'] = "Y"
            jobs.loc[i, '工作待遇_max'] = "Y"
        elif len(s_str) == 1: #一個數字
            if salary[:2] == '月薪':
                jobs.loc[i, '工作待遇_min'] = convert_num(s_str[0])
                jobs.loc[i, '工作待遇_max'] = "Y"
            elif salary[:2] == '年薪':
                jobs.loc[i, '工作待遇_min'] = convert_num(s_str[0])//13
                jobs.loc[i, '工作待遇_max'] = "Y"
        elif len(s_str) == 2: #兩個數字
            if salary[:2] == '月薪':
                jobs.loc[i, '工作待遇_min'] = convert_num(s_str[0])
                jobs.loc[i, '工作待遇_max'] = convert_num(s_str[1])
            elif salary[:2] == '年薪':
                jobs.loc[i, '工作待遇_min'] = convert_num(s_str[0])//13
                jobs.loc[i, '工作待遇_max'] = convert_num(s_str[1])//13
    
    # 管理責任
    manage = jobs.loc[i, '管理責任']
    if manage == '不需負擔管理責任':
        jobs.loc[i, '管理責任'] = 0
    elif manage == '管理人數未定' or manage == '管理4人以下':
        jobs.loc[i, '管理責任'] = 4
    elif manage == '管理5-8人':
        jobs.loc[i, '管理責任'] = 8
    elif manage =='管理9-12人':
        jobs.loc[i, '管理責任'] = 12
    elif manage == '管理13人以上':
        jobs.loc[i, '管理責任'] = 16
    
    # 上班時段
    time = jobs.loc[i, '上班時段']
    if re.findall(r_night, time) != []:
        jobs.loc[i, '上班時段'] = "輪班"
    elif re.findall(r_day, time) != []:
        jobs.loc[i, '上班時段'] = "日班"
    else:
        jobs.loc[i, '上班時段'] = "日班"
        
    # 需求人數
    people = jobs.loc[i, '需求人數']
    if people == '不限':
        jobs.loc[i, '需求人數'] = None
    else:
        jobs.loc[i, '需求人數'] = max(re.findall(r_d2, people))
    
    # 工作經歷
    year = jobs.loc[i, '工作經歷']
    
    if year == "不拘":
        jobs.loc[i, '工作經歷_數字'] = 0
    else:
        jobs.loc[i, '工作經歷_數字'] = int(re.findall(r_d2, year)[0])
        
    if year == None or year == "不拘":
        jobs.loc[i, '工作經歷'] = "0-1年"
    elif year == '1年以上' or year == "2年以上":
        jobs.loc[i, '工作經歷'] = "1-3年"
    elif year == '3年以上' or year == "4年以上":
        jobs.loc[i, '工作經歷'] = "3-5年"
    elif year == '10年以上':
        jobs.loc[i, '工作經歷'] = "10年以上"
    else:
        jobs.loc[i, '工作經歷'] = "5-10年"
        
    # 學歷要求
    if jobs.loc[i, '學歷要求'] == '不拘':
        jobs.loc[i, '學歷要求'] = '高中'
    else:
        jobs.loc[i, '學歷要求'] = jobs.loc[i, '學歷要求'][:2]
    
    # 科系要求
    dept = jobs.loc[i, "科系要求"].replace("、", " ")
    if dept == '不拘':
        dept = '教育學科類 藝術學科類 語文及人文學科類 經濟社會及心理學科類 法律學科類 商業及管理學科類 自然科學學科類 數學及電算機科學學科類 醫藥衛生學科類 工業技藝及機械學科類 工程學科類 建築及都市規劃學科類 農林漁牧學科類 家政相關學科類 運輸通信學科類 觀光服務學科類 大眾傳播學科類 其他學科類'
    dept = dept.replace('教育學科類', '綜合教育相關 普通科目教育相關 專業科目教育相關 學前教育相關 其他教育相關')
    dept = dept.replace('藝術學科類', '美術學相關 雕塑藝術相關 美術工藝相關 音樂學器相關 戲劇舞蹈相關 電影藝術相關 室內藝術相關 藝術商業設計 其他藝術相關')
    dept = dept.replace('語文及人文學科類', '本國語文相關 英美語文相關 日文相關科系 其他外國語文相關 語言學相關 歷史學相關 人類學相關 哲學相關 其他人文學相關')
    dept = dept.replace('經濟社會及心理學科類', '經濟學相關 政治學相關 社會學相關 民族學相關 心理學相關 地理學相關 區域研究相關 其他經社心理相關')
    dept = dept.replace('法律學科類', '法律相關科系')
    dept = dept.replace('商業及管理學科類', '一般商業學類 文書管理相關 會計學相關 統計學相關 資訊管理相關 企業管理相關 工業管理相關 人力資源相關 市場行銷相關 國際貿易相關 財稅金融相關 銀行保險相關 公共行政相關 其他商業及管理相關')
    dept = dept.replace('自然科學學科類', '生物學相關 化學相關 地質學相關 物理學相關 氣象學相關 海洋學相關 其他自然科學相關')
    dept = dept.replace('數學及電算機科學學科類', '一般數學相關 數理統計相關 應用數學相關 資訊工程相關 其他數學及電算機科學相關')
    dept = dept.replace('醫藥衛生學科類', '公共衛生相關 醫學系相關 中醫學系 復健醫學相關 護理助產相關 醫學技術及檢驗相關 牙醫學相關 藥學相關 醫藥工程相關 醫務管理相關 獸醫相關 其他醫藥衛生相關') 
    dept = dept.replace('工業技藝及機械學科類', '電機電子維護相關 金屬加工相關 機械維護相關 木工相關 冷凍空調相關 印刷相關 汽車汽修相關 其他工業技藝相關') 
    dept = dept.replace('工程學科類', '測量工程相關 工業設計相關 化學工程相關 材料工程相關 土木工程相關 環境工程相關 河海或船舶工程相關 電機電子工程相關 工業工程相關 礦冶工程相關 機械工程相關 航太工程相關 農業工程相關 紡織工程相關 核子工程相關 光電工程相關 其他工程相關') 
    dept = dept.replace('建築及都市規劃學科類', '建築相關 景觀設計相關 都巿規劃相關 其他建築及都市規劃學類') 
    dept = dept.replace('農林漁牧學科類', '農業相關 畜牧相關 園藝相關 植物保護相關 農業經濟相關 食品科學相關 水土保持相關 農業化學相關 林業相關 漁業相關 其他農林漁牧相關') 
    dept = dept.replace('家政相關學科類', '綜合家政相關 食品營養相關 兒童保育相關 服裝設計相關 美容美髮相關 其他家政相關') 
    dept = dept.replace('運輸通信學科類', '運輸管理相關 航空相關 航海相關 航運管理相關 通信學類 其他運輸通信相關') 
    dept = dept.replace('觀光服務學科類', '儀容服務學類 餐旅服務相關 觀光事務相關 其他觀光服務相關') 
    dept = dept.replace('大眾傳播學科類', '新聞學相關 廣播電視相關 公共關係相關 大眾傳播學相關 圖書管理相關 文物傳播相關 其他大眾傳播相關') 
    dept = dept.replace('其他學科類', '普通科 警政相關 軍事相關 體育相關 其他相關科系')
    jobs.loc[i, "科系要求"] = dept
    
    # 擅長工具
    tool = jobs.loc[i, "擅長工具"]
    if tool == "不拘":
        jobs.loc[i, "擅長工具"] = None
    elif tool == None:
        pass
    else:
        tool = re.sub(re_chinese, "", tool)
        tool = re.sub(re_space_one, "-", tool)
        tool = re.sub(re_otherword, " ", tool)
        tool = re.sub(re_space_ones, "|", tool)
        tool = "".join(words for words in tool if words.isprintable())
        jobs.loc[i, "擅長工具"] = tool
    
    # 工作技能
    # 還沒寫
    
    # 年齡分佈
    age = jobs.loc[i, '年齡分佈']
    if not pd.isnull(age):
        age = re.findall(r'\d+',jobs.loc[i, '年齡分佈'])
        age = list(map(int, age))
        if len(age) == 10:
            jobs.loc[i, '年齡分佈_小於30'] = int(sum(age[:3]))
            jobs.loc[i, '年齡分佈_大於30'] = int(sum(age[3:]))
            
    # 資本額
    money = jobs.loc[i, '資本額']
    if type(money) == float or money == "['暫不提供']": #nan
        jobs.loc[i, '資本額'] = 0
    else:
        money = money.replace('元','')
        match01 = re.findall(regex01, money)
        if match01 != []:
            m1 = match01[0]
            num1 = m1.replace('億','00000000+').replace('萬','0000').replace("'",'').replace("[",'').replace("]",'')
            num2 = num1.split('+')
            jobs.loc[i, '資本額'] = int(num2[0]) + int(num2[1])
        else:
            match02 = re.findall(regex02, money)
            if match02 != []:
                m2 = match02[0]
                num3 = m2.replace('億','00000000').replace('萬','0000').replace("'",'').replace("[",'').replace("]",'')
                jobs.loc[i, '資本額'] = int(num3)
            else:
                jobs.loc[i, '資本額'] = 0
    
    # 員工人數
    emp = jobs.loc[i, '員工人數']
    if pd.isnull(emp) or emp == "['暫不提供']" or emp[-3:] != "人']":
        jobs.loc[i, '員工人數'] = None #之後補值
    else:
        jobs.loc[i, '員工人數'] = int(re.findall(r_emp, str(emp))[0])
        
    # 公司標籤
    tag = jobs.loc[i, "公司標籤"]
    if pd.isnull(tag) or tag == "['']":
        jobs.loc[i, '公司標籤'] = ""
    else:
        tag = tag[2:-2]
        tag = tag.replace('其他', '')
        jobs.loc[i, '公司標籤'] = re.sub(r_tag, " ", tag)


#不用跑迴圈的

# 科系要求
jobs['科系要求'] = jobs['科系要求'].apply(lambda x: x.split())
dummy1 = jobs['科系要求'].str.join('|').str.get_dummies()
jobs = pd.concat([jobs, dummy1],axis=1)

# 公司標籤
jobs['公司標籤'] = jobs['公司標籤'].apply(lambda x: x.split())
dummy2 = jobs['公司標籤'].str.join('|').str.get_dummies()
jobs = pd.concat([jobs, dummy2],axis=1)
jobs = jobs.drop('公司標籤', axis=1)

# 擅長工具
tools = jobs["擅長工具"].str.get_dummies()
jobs = pd.concat([jobs, tools],axis=1)

# 員工人數
jobs['員工人數'].fillna(jobs['員工人數'].mode()[0], inplace=True)

# 需求人數
jobs['需求人數'].fillna(jobs['需求人數'].mode()[0], inplace=True)

print(jobs.head())


jobs.to_csv('job5_all_clean.csv',index=None, encoding="utf_8_sig")