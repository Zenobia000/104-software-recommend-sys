import numpy as np
import pandas as pd

df = pd.read_csv('./job7_all_clean.csv',encoding='utf-8-sig')
df = df.dropna().reset_index(drop=True)

edu_dict = {'高中':18,'專科':20, '大學':22, '碩士':25, '博士':30}
df['學歷要求'] = df['學歷要求'].map(edu_dict)

working_time = {"日班":1,'輪班':2}
df["上班時段_label"] = df['上班時段'].map(working_time)

tw_region_label = {"臺北市":1,"新北市":2,"臺中市":3,"新竹市":4,"桃園市":5,"高雄市":6,"新竹縣":7, '新竹市':8,"臺南市":9,"苗栗縣":10
,"彰化縣":11,"雲林縣":12,"宜蘭縣":13,"嘉義縣":14,"花蓮縣":15,"屏東縣":16,"南投縣":17,"嘉義市":18,"基隆市":19,
"金門縣":20,"臺東縣":21,"澎湖縣":22, "連江縣":23}
df['縣市_label'] = df["縣市"].map(tw_region_label)

pst_label = {"軟體_工程類人員" : 1, "MIS_網管類人員":2}
df["職位類別_label"] = df['職位類別'].map(pst_label)

df["管理責任_"] = None
df["學歷要求_"] = None
df["需求人數_"] = None
df['職位_'] = None

for i in range(len(df.values)):
            # 管理責任
    manage = df.loc[i, '管理責任']
    if manage == 0 or manage == 4:
        df.loc[i, '管理責任_'] = "管理 0-4 人"
    elif manage == 8 or manage == 12:
        df.loc[i, '管理責任_'] = "管理 5-12 人"
    elif manage == 16:
        df.loc[i, '管理責任_'] = "管理 13 人以上"

    # {'高中':18,'專科':20, '大學':22, '碩士':25, '博士':30}
    edu = df.loc[i, '學歷要求']
    if edu == 18 or edu == 20 or edu == 22:
        df.loc[i, '學歷要求_'] = "高中-專科-大學"
    elif edu == 25:
        df.loc[i, '學歷要求_'] = "碩士"
    elif edu == 30:
        df.loc[i, '學歷要求_'] = "博士"

    # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
    # 12, 13, 15, 18, 20, 21, 25, 30, 50, 51, 80, 99}
    demand = df.loc[i, '需求人數']
    if demand < 10:
        df.loc[i, '需求人數_'] = "需求 0-9 人"
    elif demand >= 10 and demand < 15:
        df.loc[i, '需求人數_'] = "需求 10-14 人"
    elif demand >= 15:
        df.loc[i, '需求人數_'] = "需求 15 人以上"

    # {'MIS程式設計師', '軟體專案主管', 'MES工程師', '資訊設備管制人員', 
    # '資料庫管理人員', '系統分析師', 'Internet程式設計師', 'BIOS工程師', 
    # '其他資訊專業人員', '演算法開發工程師', '網路安全分析師', '資訊助理人員', 
    # '通訊軟體工程師', '系統維護_操作人員', '網路管理工程師', '韌體設計工程師', 
    # 'MIS_網管主管', '電子商務技術主管', '電玩程式設計師', '軟體設計工程師'}

    grp1 = ['BIOS工程師']
    grp2 = ['電玩程式設計師','演算法開發工程師', 'Internet程式設計師', '軟體設計工程師']
    grp3 = ['系統分析師', 'MIS_網管主管', '系統維護_操作人員', '韌體設計工程師','資料庫管理人員',
    '資訊助理人員', 'MIS程式設計師', '其他資訊專業人員', '網路管理工程師', '資訊設備管制人員']
    grp4 = ['網路安全分析師', 'MES工程師', '通訊軟體工程師','軟體專案主管', '電子商務技術主管' ]

    pst = df.loc[i, '職位']
    if pst in grp2:
        df.loc[i, '職位_'] = "職位 II"
    elif pst in grp3:
        df.loc[i, '職位_'] = "職位 III"
    elif pst in grp4:
        df.loc[i, '職位_'] = "職位 IV"
    elif pst in grp1:
        df.loc[i, "職位_"] = '職位 I'
    
df.to_csv('df_4groups.csv', encoding='utf-8-sig')