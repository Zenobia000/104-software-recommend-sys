import os

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing
from sklearn import neighbors, datasets
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import GridSearchCV
import xgboost as xgb

import matplotlib.pyplot as plt

df = pd.read_csv('./job7_4groups.csv',encoding='utf-8-sig')

# get dummies
# df_pst = pd.get_dummies(df['職位'])
df_pst_ = pd.get_dummies(df['職位_'])
df_pst_cat = pd.get_dummies(df['職位類別'])
df_country = pd.get_dummies(df['縣市'])
df_area = pd.get_dummies(df['地區'])
df_time = pd.get_dummies(df['上班時段'])

df_edu_ = pd.get_dummies(df['學歷要求_'])
df_res_ = pd.get_dummies(df['管理責任_'])
df_dem_ = pd.get_dummies(df['需求人數_'])
df_work_ = pd.get_dummies(df['工作經歷'])
# df_pst_cat_ = pd.get_dummies(df['職位類別'])
# df_county_ = pd.get_dummies(df['縣市'])
# df_area_ = pd.get_dummies(df['地區'])
# df_time_ = pd.get_dummies(df['上班時段'])

#擅長工具
df_tools = (df.iloc[:,193:-4]).copy()
df = df.astype({'供需人數':'int64'})

# label encoding
col_list = ['職位類別_label', '縣市_label', '上班時段_label', '外商', '供需人數', '工作待遇_min']
df_ = df.loc[:, col_list].reset_index(drop=True)
df_label = pd.concat([df_, df_pst_, df_area, df_edu_, df_res_, df_dem_, df_work_, df_tools], axis=1)
df_label = df_label.drop(df_label[pd.isnull(df_label["工作待遇_min"])].index)
df_label = df_label.drop(df_label[df_label["工作待遇_min"] == 'Y'].index)
df_label = df_label.astype({"工作待遇_min":'int64'})

# get dummies
col_list2 = ['外商', '供需人數', '工作待遇_min']
df2_ = df.loc[:, col_list2].reset_index(drop=True)
df_dummies = pd.concat([df2_, df_pst_cat, df_pst_, df_country, df_area, df_time,
                        df_edu_, df_res_, df_dem_, df_work_, df_tools], axis=1)
df_dummies = df_dummies.drop(df_dummies[pd.isnull(df_dummies["工作待遇_min"])].index)
df_dummies = df_dummies.drop(df_dummies[df_dummies["工作待遇_min"] == 'Y'].index)
df_dummies = df_dummies.astype({"工作待遇_min":'int64'})

# 兩種版本
df_test_select = df_label.copy()
# df_test_select = df_dummies.copy()

# split data
y = df_test_select['工作待遇_min']
X = df_test_select.drop('工作待遇_min',axis=1).copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

lasso_df = pd.DataFrame(columns = ['model', 'data', 'case', 'alpha', 'iteration', 'cv', 'r^2', 'mse', 'accuracy'])

# Lasso
a = [0.1, 0.5, 1, 10, 25, 50, 100]
mi = [20000, 50000, 80000, 100000]
# c = [3, 5, 10]

for i in range(len(a)):
    for j in range(len(mi)):
        
        model = linear_model.Lasso(alpha=a[i], max_iter = mi[j])
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        
        new_row = {'model': 'Lasso', 
                   'data': '3w', 
                   'case': 'dummies', 
                   'alpha': a[i], 
                   'iteration': mi[j], 
                   'cv': None, 
                   'r^2': r2, 
                   'mse': mse, 
                   'accuracy': None}
        lasso_df = lasso_df.append(new_row, ignore_index=True)

        print('Lasso alpha =', a[i], 'iteration =', mi[j],
              'MSE: {}'.format((mse)), 'R2: {}'.format(r2))

lasso_df.to_csv('lasso_df_v2.csv')