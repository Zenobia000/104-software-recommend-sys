import os

import numpy as np
import pandas as pd

import seaborn as sns

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties as font

df = pd.read_csv('job7_4groups.csv',encoding='utf-8-sig')

df_heatmap = df[['縣市','職位','管理責任','上班時段','工作經歷_數字','工作經歷','職位類別','需求人數','供需人數','外商','地區','學歷要求','工作待遇_min']]
df_heatmap = df_heatmap.drop(df[df["工作待遇_min"] == 'Y'].index)
df_heatmap = df_heatmap.drop(df[pd.isnull(df["工作待遇_min"])].index)
df_heatmap = df_heatmap.astype({"工作待遇_min":'int64'})
df_heatmap

df_heatmap_data = pd.pivot_table(df_heatmap, values='工作待遇_min',
                            index=['工作經歷'],
                            columns='縣市',fill_value=0)
df_heatmap_data.head()

print(matplotlib.matplotlib_fname())
print(matplotlib.get_cachedir())

plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
# plt.rcParams['font.family']='sans-serif' 
# plt.rcParams['axes.unicode_minus'] = False


# make heatmap with Seaborn ClusterMap
sns.clustermap(df_heatmap_data)
plt.savefig('heatmap_with_Seaborn_clustermap_工作經歷_類別_縣市.jpg',
            dpi=150)