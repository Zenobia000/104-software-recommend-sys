# import
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

# driver
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")  # 最大化視窗
my_options.add_argument("--incognito")  # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  # 設定為正體中文

driver = webdriver.Chrome(
    options=my_options,
    service=Service(ChromeDriverManager().install())
)

# city
city = ['臺北市', '新北市', '宜蘭縣', '基隆市', '桃園市', '新竹縣', '苗栗縣', '臺中市', '無縣市', '彰化縣',
        '南投縣', '雲林縣', '嘉義縣', '臺南市', '無縣市', '高雄市', '無縣市', '屏東縣', '臺東縣', '花蓮縣',
        '澎湖縣', '金門縣', '連江縣']
# districts
# ndistrict = [12, 29, 12, 7, 13, 14, 18, 29, 0, 26,
#             13, 20, 19, 37, 0, 38, 0,  33, 16, 13,
#             6, 6, 4]

district = [
    ["中正區", "大同區", "中山區", "松山區", "大安區", "萬華區", "信義區", "士林區", "北投區", "內湖區",
     "南港區", "文山區"],

    ["萬里區", "金山區", "板橋區", "汐止區", "深坑區", "石碇區", "瑞芳區", "平溪區", "雙溪區", "貢寮區",
     "新店區", "坪林區", "烏來區", "永和區", "中和區", "土城區", "三峽區", "樹林區", "鶯歌區", "三重區",
     "新莊區", "泰山區", "林口區", "蘆洲區", "五股區", "八里區", "淡水區", "三芝區", "石門區"],

    ["宜蘭市", "頭城鎮", "礁溪鄉", "壯圍鄉", "員山鄉", "羅東鎮", "三星鄉", "大同鄉", "五結鄉", "冬山鄉",
     "蘇澳鎮", "南澳鄉"],

    ["仁愛區", "信義區", "中正區", "中山區", "安樂區", "暖暖區", "七堵區"],

    ["中壢區", "平鎮區", "龍潭區", "楊梅區", "新屋區", "觀音區", "桃園區", "龜山區", "八德區", "大溪區",
     "復興區", "大園區", "蘆竹區"],

    ["新竹市", "竹北市", "湖口鄉", "新豐鄉", "新埔鎮", "關西鎮", "芎林鄉", "寶山鄉", "竹東鎮", "五峰鄉",
     "橫山鄉", "尖石鄉", "北埔鄉", "峨眉鄉"],

    ["竹南鎮", "頭份市", "三灣鄉", "南庄鄉", "獅潭鄉", "後龍鎮", "通霄鎮", "苑裡鎮", "苗栗市", "造橋鄉",
     "頭屋鄉", "公館鄉", "大湖鄉", "泰安鄉", "銅鑼鄉", "三義鄉", "西湖鄉", "卓蘭鎮"],


    ["中區", "東區", "南區", "西區", "北區", "北屯區", "西屯區", "南屯區", "太平區", "大里區", "霧峰區", "烏日區", "豐原區",
     "后里區", "石岡區", "東勢區", "和平區", "新社區", "潭子區", "大雅區", "神岡區", "大肚區", "沙鹿區", "龍井區", "梧棲區",
     "清水區", "大甲區", "外埔區", "大安區"],

    [],

    ["彰化市", "芬園鄉", "花壇鄉", "秀水鄉", "鹿港鎮", "福興鄉", "線西鄉", "和美鎮", "伸港鄉", "員林市", "社頭鄉", "永靖鄉",
     "埔心鄉", "溪湖鎮", "大村鄉", "埔鹽鄉", "田中鎮", "北斗鎮", "田尾鄉", "埤頭鄉", "溪州鄉", "竹塘鄉", "二林鎮", "大城鄉",
     "芳苑鄉", "二水鄉"],

    ["南投市", "中寮鄉", "草屯鎮", "國姓鄉", "埔里鎮", "仁愛鄉", "名間鄉", "集集鎮", "魚池鄉", "水里鄉", "信義鄉", "竹山鎮",
     "鹿谷鄉"],

    ["斗南鎮", "大埤鄉", "虎尾鎮", "土庫鎮", "褒忠鄉", "東勢鄉",  "臺西鄉", "崙背鄉", "麥寮鄉", "斗六市", "林內鄉", "古坑鄉",
     "莿桐鄉", "西螺鎮", "二崙鄉", "北港鎮", "水林鄉", "口湖鄉", "四湖鄉", "元長鄉"],

    ['嘉義市', '番路鄉', '梅山鄉', '竹崎鄉', '阿里山鄉', '中埔鄉', '大埔鄉', '水上鄉', '鹿草鄉', '太保市', '朴子市', '東石鄉',
     '六腳鄉', '新港鄉', '民雄鄉', '大林鎮', '溪口鄉', '義竹鄉', '布袋鎮'],

    ["中西區", "東區", "南區", "北區", "安平區", "安南區", "永康區", "歸仁區", "新化區", "左鎮區", "玉井區", "楠西區", "南化區",
     "仁德區", "關廟區", "龍崎區", "官田區", "麻豆區", "佳里區", "西港區", "七股區", "將軍區", "學甲區", "北門區", "新營區",
     "後壁區", "白河區", "東山區", "六甲區", "下營區", "柳營區", "鹽水區", "善化區", "大內區", "山上區", "新市區", "安定區"],

    [],

    ['新興區', '前金區', '苓雅區', '鹽埕區', '鼓山區', '旗津區', '前鎮區', '三民區', '楠梓區', '小港區', '左營區', '仁武區', '大社區',
     '岡山區', '路竹區', '阿蓮區', '田寮區', '燕巢區', '橋頭區', '梓官區', '彌陀區', '永安區', '湖內區', '鳳山區', '大寮區', '林園區',
     '鳥松區', '大樹區', '旗山區', '美濃區', '六龜區', '內門區', '杉林區', '甲仙區', '桃源區', '那瑪夏區', '茂林區', '茄萣區'],

    [],
    ['屏東市', '三地門鄉', '霧臺鄉', '瑪家鄉', '九如鄉', '里港鄉', '高樹鄉', '鹽埔鄉', '長治鄉', '麟洛鄉', '竹田鄉', '內埔鄉',
     '萬丹鄉', '潮州鎮', '泰武鄉', '來義鄉', '萬巒鄉', '崁頂鄉', '新埤鄉', '南州鄉', '林邊鄉', '東港鎮', '琉球鄉',  '佳冬鄉',
     '新園鄉', '枋寮鄉', '枋山鄉', '春日鄉', '獅子鄉', '車城鄉', '牡丹鄉', '恆春鎮', '滿州鄉'],

    ['臺東市', '綠島鄉', '蘭嶼鄉', '延平鄉', '卑南鄉', '鹿野鄉',  '關山鎮', '海端鄉', '池上鄉', '東河鄉', '成功鎮', '長濱鄉', '太麻里鄉',
     '金峰鄉', '大武鄉', '達仁鄉'],

    ['花蓮市', '新城鄉', '秀林鄉', '吉安鄉', '壽豐鄉', '鳳林鎮', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉',
     '玉里鎮', '卓溪鄉', '富里鄉'],

    ['馬公市', '西嶼鄉', '望安鄉', '七美鄉', '白沙鄉', '湖西鄉'],

    ['金沙鎮', '金湖鎮', '金寧鄉', '金城鎮', '烈嶼鄉', '烏坵鄉'],

    ['南竿鄉', '北竿鄉', '莒光鄉', '東引鄉']
]


# job
# 所有編號 2維矩陣
job_list = [['2017001001', '2017001002', '2017001003', '2017001004'],

             ['2017002001', '2017002002', '2017002003', '2017002005', '2017002004']]

# 中類別名稱
job_name1 = ['軍警消防類人員', '保全類人員']
# 小類別名稱
job_name2 = [['志願役軍官_士官／士兵', '消防專業人員', '消防員', '救生員'],

              ['保全人員_警衛', '保全技術人員', '大樓管理員', '總幹事', '其他保安服務工作']]


def inputlink():
    links = driver.find_elements(
        By.CSS_SELECTOR, "li.job-mode__jobname > a"
    )
    for link in links:
        href = link.get_attribute('href')
        alinks.append(href)

    # batterys
    use_selectors = driver.find_elements(
        By.CSS_SELECTOR,
        'ul > li.job-mode__candidates.js-apply-cnt > a > svg > use'
    )
    for use in use_selectors:
        battery = use.get_attribute('xlink:href')[-1]
        batterys.append(battery)

    if len(alinks) != len(batterys):
        print("第"+str(i)+"頁有誤！")


def craw(i):  # by noah
    b = int(batterys[i])
    try:
        # 等待篩選元素出現
        IDN = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 'div.job-header__btn.mb-3 > div > form > input[type=hidden]:nth-child(1)')
            )
        )
    except TimeoutException:  # invalid link
        result = {
            '職缺連結': None,
            '職缺類別': None,
            '職位類別': None,
            '職位': None,
            '大職業編號': None,
            '中職業編號': None,
            '小職業編號': None,
            '縣市': None,
            '地區': None,
            '縣市編碼': None,
            '地區編碼': None,
            '公司連結': None,
            '供需人數': None,
            '職缺編號': None,
            '公司名稱': None,
            '職缺名稱': None,
            '更新日期': None,
            '工作內容': None,
            '職務類別': None,
            '工作待遇': None,
            '工作性質': None,
            '上班地點': None,
            '管理責任': None,
            '上班時段': None,
            '需求人數': None,
            '工作經歷': None,
            '學歷要求': None,
            '科系要求': None,
            '擅長工具': None,
            '工作技能': None,
            '其他條件': None,
            '福利制度': None,
            '資本額': None,
            '員工人數': None,
            '公司內文': None
        }
        results.append(result)
        return

    IDN = driver.find_element(
        By.CSS_SELECTOR, 'div.job-header__btn.mb-3 > div > form > input[type=hidden]:nth-child(1)').get_attribute('value')
    workname = driver.find_element(
        By.CSS_SELECTOR, 'div.job-header__title>h1').get_attribute("innerText")
    workupdate = driver.find_element(
        By.CSS_SELECTOR, 'div.job-header__title>h1>span').get_attribute("innerText")
    work = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]').get_attribute("innerText")
    companymame = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[1]/div/a[1]').get_attribute("innerText")
    company_link = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[1]/div/a[1]').get_attribute('href')
    workclass = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]').get_attribute("innerText")
    salary = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]').get_attribute("innerText")
    xìngzhì = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[4]/div[2]/div').get_attribute("innerText")
    locate = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[5]/div[2]/div').get_attribute("innerText")
    responsibility = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[7]/div[2]').get_attribute("innerText")
    workhr = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[9]/div[2]').get_attribute("innerText")

    try:
        needp = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(10) > div.col.p-0.list-row__data > div'))
        )
        needp = driver.find_element(
            By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[1]/div[2]/div[12]/div[2]').get_attribute("innerText")

    except:
        needp = driver.find_element(
            By.CSS_SELECTOR, 'div.job-description-table.row > div:nth-child(9) > div.col.p-0.list-row__data > div').get_attribute("innerText")

    experience = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div').get_attribute("innerText")
    Education = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div').get_attribute("innerText")
    DPR = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div').get_attribute("innerText")
    tools = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[2]/div[5]/div[2]/div').get_attribute("innerText")
    wskills = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[2]/div[6]/div[2]/div').get_attribute("innerText")
    others = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/p').get_attribute("innerText")
    otherss = others.replace('\n', '')

    # Welfare =driver.find_elements(By.CSS_SELECTOR,'div.col > p.r3.mb-0.text-break')
    try:
        Welfare = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.col > p.r3.mb-0.text-break"))
        )
        Welfare = driver.find_element(
            By.CSS_SELECTOR, 'div.col > p.r3.mb-0.text-break').get_attribute('innerText')
    except:
        Welfare = None

    workk = work.replace('\n', '')
    fwork = workk.replace('-', '')

    if b == 1:
        people = 2.5
    elif b == 2:
        people = 7.5
    elif b == 3:
        people = 20
    elif b == 4:
        people = 60
    else:
        print("battery wrong")

    if Welfare != None:
        result = {
            '職缺連結': alinks[i],
            '職缺類別': a1,  # '經營_人資類'
            '職位類別': a2,  # '經營_幕僚類人員'
            '職位': a3,  # '儲備幹部'
            '大職業編號': a_large,
            '中職業編號': a_med,
            '小職業編號': a_small,
            '縣市': a4,  # '新北市'
            '地區': a5,  # '板橋區'
            '縣市編碼': a_city,
            '地區編碼': a_district,
            '公司連結': company_link,
            '供需人數': people,
            '職缺編號': IDN,
            '公司名稱': companymame,
            '職缺名稱': workname,
            '更新日期': workupdate,
            '工作內容': fwork,
            '職務類別': workclass.replace('\n', ''),
            '工作待遇': salary.replace('\n', ''),
            '工作性質': xìngzhì,
            '上班地點': locate,
            '管理責任': responsibility,
            '上班時段': workhr,
            '需求人數': needp,
            '工作經歷': experience,
            '學歷要求': Education,
            '科系要求': DPR,
            '擅長工具': tools.replace('\n', ''),
            '工作技能': wskills,
            '其他條件': otherss.replace('\t', ''),
            '福利制度': Welfare.replace('\n', ''),
        }

    else:
        result = {
            '職缺連結': alinks[i],
            '職缺類別': a1,  # '經營_人資類'
            '職位類別': a2,  # '經營_幕僚類人員'
            '職位': a3,  # '儲備幹部'
            '大職業編號': a_large,
            '中職業編號': a_med,
            '小職業編號': a_small,
            '縣市': a4,  # '新北市'
            '地區': a5,  # '板橋區'
            '縣市編碼': a_city,
            '地區編碼': a_district,
            '公司連結': company_link,
            '供需人數': people,
            '職缺編號': IDN,
            '公司名稱': companymame,
            '職缺名稱': workname,
            '更新日期': workupdate,
            '工作內容': fwork,
            '職務類別': workclass.replace('\n', ''),
            '工作待遇': salary.replace('\n', ''),
            '工作性質': xìngzhì,
            '上班地點': locate,
            '管理責任': responsibility,
            '上班時段': workhr,
            '需求人數': needp,
            '工作經歷': experience,
            '學歷要求': Education,
            '科系要求': DPR,
            '擅長工具': tools.replace('\n', ''),
            '工作技能': wskills,
            '其他條件': otherss.replace('\t', ''),
            '福利制度': Welfare
        }

    # 11/21 新增
    # 去電池內文
    battery_link = driver.find_element(
        By.CSS_SELECTOR, 'div.job-header__status.text-gray-darker.text-right.t4 > a').get_attribute('href')
    driver.get(battery_link)
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div:nth-child(1) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td")))

        etxt1 = driver.find_element(
            By.CSS_SELECTOR, 'div:nth-child(1) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td')
        Boshuoshì = etxt1.get_attribute('innerText')
        etxt2 = driver.find_element(
            By.CSS_SELECTOR, 'div:nth-child(1) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td')
        Daxue = etxt2.get_attribute('innerText')
        etxt3 = driver.find_element(
            By.CSS_SELECTOR, 'div:nth-child(1) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td')
        Zhuanke = etxt3.get_attribute('innerText')
        etxt4 = driver.find_element(
            By.CSS_SELECTOR, 'div:nth-child(1) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td')
        Gaozhongzhi = etxt4.get_attribute('innerText')
        etxt5 = driver.find_element(
            By.CSS_SELECTOR, 'div:nth-child(1) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(5) > td')
        below = etxt5.get_attribute('innerText')

        atxt1 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(1) > td > div > div.text.t3.ml-2.ml-md-4')
        below20 = atxt1.get_attribute('innerText')
        atxt2 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(2) > td > div > div.text.t3.ml-2.ml-md-4')
        between2125 = atxt2.get_attribute('innerText')
        atxt3 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(3) > td > div > div.text.t3.ml-2.ml-md-4')
        between2630 = atxt3.get_attribute('innerText')
        atxt4 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(4) > td > div > div.text.t3.ml-2.ml-md-4')
        between3135 = atxt4.get_attribute('innerText')
        atxt5 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(5) > td > div > div.text.t3.ml-2.ml-md-4')
        between3640 = atxt5.get_attribute('innerText')
        atxt6 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(6) > td > div > div.text.t3.ml-2.ml-md-4')
        between4145 = atxt6.get_attribute('innerText')
        atxt7 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(7) > td > div > div.text.t3.ml-2.ml-md-4')
        between4650 = atxt7.get_attribute('innerText')
        atxt8 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(8) > td > div > div.text.t3.ml-2.ml-md-4')
        between5155 = atxt8.get_attribute('innerText')
        atxt9 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(9) > td > div > div.text.t3.ml-2.ml-md-4')
        between5560 = atxt9.get_attribute('innerText')
        atxt10 = driver.find_element(
            By.CSS_SELECTOR, ' div.col-12.col-md-6.mt-3.mt-md-4 > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > table > tbody > tr:nth-child(10) > td > div > div.text.t3.ml-2.ml-md-4')
        up60 = atxt10.get_attribute('innerText')

        gtxt1 = driver.find_element(
            By.CSS_SELECTOR, ' div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td')
        male = gtxt1.get_attribute('innerText')
        gtxt2 = driver.find_element(
            By.CSS_SELECTOR, ' div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5 > div > div:nth-child(1) > table > tbody > tr:nth-child(2) > td')
        female = gtxt2.get_attribute('innerText')

        wtxt1 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(1) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        nworkexp = wtxt1.get_attribute('innerText')
        wtxt2 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(2) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow1 = wtxt2.get_attribute('innerText')
        wtxt3 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(3) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow13 = wtxt3.get_attribute('innerText')
        wtxt4 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(4) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow35 = wtxt4.get_attribute('innerText')
        wtxt5 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(5) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow510 = wtxt5.get_attribute('innerText')
        wtxt6 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(6) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow1015 = wtxt6.get_attribute('innerText')
        wtxt7 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(7) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow1520 = wtxt7.get_attribute('innerText')
        wtxt8 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(8) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wbelow2025 = wtxt8.get_attribute('innerText')
        wtxt9 = driver.find_element(
            By.CSS_SELECTOR, 'div > div:nth-child(9) > div.vertical-bar.vertical-bar-chart__bar > div.text.t3.text-center.mt-2')
        wup25 = wtxt9.get_attribute('innerText')
        langzone = driver.find_element(
            By.CSS_SELECTOR, '#app > div.container > div.analysis > div:nth-child(3) > div:nth-child(1) > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5').get_attribute('innerText')
        langzone1 = langzone.replace('\t', '')
        langzone2 = langzone1.replace('\n\n', ',')
        langzone3 = langzone2.replace('\n', '')
        langzone3

        kexizone = driver.find_element(
            By.CSS_SELECTOR, '#app > div.container > div.analysis > div:nth-child(3) > div:nth-child(2) > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5').get_attribute('innerText')
        kexizone1 = kexizone.replace('\t', '')
        kexizone2 = kexizone1.replace('\n\n', ',')
        kexizone3 = kexizone2.replace('\n', '')

        skillzone = driver.find_element(
            By.CSS_SELECTOR, '#app > div.container > div.analysis > div:nth-child(3) > div:nth-child(3) > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5').get_attribute('innerText')
        skillzone1 = skillzone.replace('\t', '')
        skillzone2 = skillzone1.replace('\n\n', ',')
        skillzone3 = skillzone2.replace('\n', ' ')
        skillzone3

        licensezone = driver.find_element(
            By.CSS_SELECTOR, '#app > div.container > div.analysis > div:nth-child(3) > div:nth-child(4) > div > div.information.overflow-auto.px-4.px-md-0.d-md-block.pr-md-5').get_attribute('innerText')
        licensezone1 = licensezone.replace('\t', '')
        licensezone2 = licensezone1.replace('\n\n', ',')
        licensezone3 = licensezone2.replace('\n', ' ')

        result['學歷分佈'] = [Boshuoshì, Daxue, Zhuanke, Gaozhongzhi, below]
        result['性別分佈'] = [male, female]
        result['工作經驗分佈'] = [wup25, wbelow2025, wbelow1520, wbelow1015,
                            wbelow510, wbelow35, wbelow13, wbelow1, nworkexp]
        result['年齡分佈'] = [up60, between5560, between5155, between4650,
                          between4145, between3640, between3135, between2630, between2125, below20]
        result['語言能力分佈'] = [langzone3]
        result['科系分佈'] = [kexizone3]
        result['技能分佈'] = [skillzone3]
        result['證照分佈'] = [licensezone3]

    except:
        print('電池內文壞了')
        result['學歷分佈'] = None
        result['性別分佈'] = None
        result['工作經驗分佈'] = None
        result['年齡分佈'] = None
        result['語言能力分佈'] = None
        result['科系分佈'] = None
        result['技能分佈'] = None
        result['證照分佈'] = None

    driver.get(company_link)
    sleep(0.5)
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div > div:nth-child(3) > div:nth-child(2) > p")))

    capital_amount2 = driver.find_element(
        By.CSS_SELECTOR, 'div > div:nth-child(3) > div:nth-child(2) > p').get_attribute('innerText')
    capital_amount1 = capital_amount2.split(' ')
    conpany_people = driver.find_element(
        By.CSS_SELECTOR, ' div > div:nth-child(4) > div:nth-child(2) > p').get_attribute('innerText')
    try:
        conpany_text = driver.find_element(
            By.CSS_SELECTOR, ' #intro > div.row.intro-description > div > p').get_attribute('innerText')
        conpany_text1 = conpany_text.replace('\t', '')
        conpany_text3 = (conpany_text1.replace('\n', ' ')).replace('\r', '')
        try:
            conpany_texts = (((driver.find_element(
                By.CSS_SELECTOR, ' #intro > div.row.intro-management').get_attribute('innerText')).replace('\t', '')).replace('\n', ' ')).replace('\r', '')
            conpany_text3 = conpany_text3 + ' ' + conpany_texts
        except:
            print('no conpany_texts')
            
        try:
            company_tag = driver.find_elements(By.CSS_SELECTOR, 'div.header__nav__title.py-8 > div > div > a')
            company_tag_text = ''
            for i in company_tag:
                company_tag_text += i.get_attribute('innerText')
        except:
            print('no company_tag')
            
    except:
        print('error')

    result['資本額'] = [capital_amount1[0]]
    result['員工人數'] = [conpany_people]
    result['公司內文'] = [conpany_text3]
    result['公司標籤'] = [company_tag_text]

    results.append(result)
#     sleep(0.5)


# main
for i in range(len(city)):

    city_id = i+1
    city_str = "0"+str(city_id) if city_id < 10 else str(city_id)

    for j in range(len(district[i])):

        district_id = j+1
        district_str = "0" + str(district_id) if district_id < 10 else str(district_id)

        for jobi in range(len(job_list)):
            for jobj in range(len(job_list[jobi])):

                job_num = job_list[jobi][jobj]

                alinks = []
                batterys = []
                results = []

                for p in range(1, 101):  # suppose 100 pages
                    url = 'https://www.104.com.tw/jobs/search/?ro=0&jobcat=' + job_num + '&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=60010' + city_str + '0' + district_str + '&order=4&asc=0&page=' + str(p) + '&mode=l&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
                    driver.get(url)
                    sleep(0.5)
                    
                    if p == 1:
                        # total links
                        totallinks_str = driver.find_elements(
                            By.CSS_SELECTOR, '#js-job-tab > li.b-nav-tabs__active > span')[0].text
                        totallinks_num = int(totallinks_str[1:-1])
                        
                    try:
                        check_if_there_is_link = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'li.job-mode__jobname > a')))
                    except TimeoutException:  # no links, it's last page
                        last_page = p-1
                        break

                    # not last page
                    
                    inputlink()

                a1 = '軍警消_保全類'
                a2 = job_name1[jobi]
                a3 = job_name2[jobi][jobj]
                a_large = 16
                a_med = int(job_num[5:7])
                a_small = int(job_num[8:])
                a4 = city[i]
                if i == 5 and j == 0:
                    a4 = '新竹市'
                if i == 12 and j == 0:
                    a4 = '嘉義市'
                a5 = district[i][j]
                a_city = city_id
                a_district = district_id

                # run all alinks to get job detail
                for l, link in enumerate(alinks[:totallinks_num]):
                    driver.get(link)
                    print(l+1, end=", ")
#                     sleep(0.2)
                    craw(l)

                # save json/csv
                filename_innerText = job_num+'_'+city_str+district_str
                with open(f'{filename_innerText}'+'.json', "w", encoding='utf-8') as file:
                    file.write(json.dumps(
                        results, ensure_ascii=False, indent=4))
                print("檔案", filename_innerText, " ",
                      str(last_page)+"頁",
                      str(totallinks_num)+"筆", "下載完畢")

                df = pd.read_json(filename_innerText+'.json')
                df.to_csv(filename_innerText+'.csv',
                   index=None, encoding="utf_8_sig")


driver.quit()


