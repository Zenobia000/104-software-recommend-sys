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

# %%
# Fit linear regression model
lr = LinearRegression(random_state=2022, feature_names=X.columns)
lr.fit(X_train, y_train, )
print("Training finished.")


# Evaluate linear regression model
y_pred = lr.predict(X_test)
print(f"Root Mean Squared Error: {round(mean_squared_error(y_test, y_pred)**(1/2), 2)}")
print(f"R2: {round(r2_score(y_test, y_pred), 2)}")

# %%
# Fit decision tree model for regression
rt = RegressionTree(random_state=2022, max_depth=6)
rt.fit(X_train, y_train)
print("Training finished.")

# Evaluate decision tree model for regression
y_pred = rt.predict(X_test)
print(f"Root Mean Squared Error: {round(mean_squared_error(y_test, y_pred)**(1/2), 2)}")
print(f"R2: {round(r2_score(y_test, y_pred), 2)}")

# %%
# Fit explainable boosting machine for regression
ebr = ExplainableBoostingRegressor(random_state=2022)
ebr.fit(X_train, y_train) 
print("Training finished.")

# Evaluate explainable boosting machine for regression
y_pred = ebr.predict(X_test)
print(f"Root Mean Squared Error: {round(mean_squared_error(y_test, y_pred)**(1/2), 2)}")
print(f"R2: {round(r2_score(y_test, y_pred), 2)}")

# %%


# %%
lasso_df = pd.DataFrame(columns = ['model', 'data', 'case', 'alpha', 'iteration', 'cv', 'r^2', 'mse', 'accuracy'])

# %%
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

# %%
lasso_df

# %%
lasso_df.to_csv('lasso_df_v2.csv')

# %%


# %%
# Ridge

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

model = linear_model.Ridge(alpha=1.0, max_iter = 100000)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print('Ridge\n')
print("Mean squared error: {}".format((mean_squared_error(y_test, y_pred))))
print('R2 score: {}'.format(r2_score(y_test, y_pred)))
print('number of model coef: {}'.format(np.sum(model.coef_ != 0)))

# %%
# Elastic

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

model = linear_model.ElasticNet(alpha=1.0, l1_ratio=0.5, l2_ratio = 1, max_iter = 100000)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print('Elastic\n')
print("Mean squared error: {}".format((mean_squared_error(y_test, y_pred))))
print('R2 score: {}'.format(r2_score(y_test, y_pred)))
print('number of model coef: {}'.format(np.sum(model.coef_ != 0)))

# %%
# KNN

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


model = neighbors.KNeighborsClassifier(n_neighbors=3)   # KNN K值是3
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
num_correct_samples = accuracy_score(y_test, y_pred, normalize=False)
con_matrix = confusion_matrix(y_test, y_pred)

print('KNN\n')
print('number of correct sample: {}'.format(num_correct_samples))
print('accuracy: {}'.format(accuracy))
print('confusion matrix: {}'.format(con_matrix))

# %%
# Random Forest

os.environ["PATH"] += os.pathsep + 'C:/Users/student/Desktop/BDSE_機器學習/ands-on_part5/example/example/release/bin'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)


model = RandomForestRegressor(max_depth=3, random_state=0)
model.fit(X_train, y_train)

X_test = scaler.transform(X_test)
y_pred = model.predict(X_test)



mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


print('Random Forest:')
print('R-squared: {}'.format(r2))
print('MSE: {}'.format(mse))

# %%
# Bagging Boost

from sklearn.ensemble import BaggingRegressor
from sklearn import metrics

ensemble = BaggingRegressor(n_estimators=1000)

ensemble.fit(X_train, y_train)
predictions = ensemble.predict(X_test)

r2 = metrics.r2_score(y_test, predictions)
mse = metrics.mean_squared_error(y_test, predictions)

print('Gradient Boosting:')
print('R-squared: {}'.format(r2))
print('MSE: {}'.format(mse))

# %%
# XGBoost
regressor = xgb.XGBRegressor(n_estimators = 2000, reg_lambda = 50, gamma = 0, max_depth = 9)

regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print('XG Boosting:')
print('R-squared: {}'.format(r2))
print('MSE: {}'.format(mse))

# %%
import sklearn

print(sklearn.metrics.SCORERS.keys())

# %%
from sklearn.model_selection import StratifiedKFold
kn = xgb.XGBRegressor()
params = {'n_estimators':[1000],'reg_lambda':[1],'gamma':[0],'max_depth':range(3, 10)}

scoring = ['r2','neg_mean_squared_error','neg_root_mean_squared_error']



grid_kn = GridSearchCV(estimator = kn,
                        param_grid = params,
                        cv = 5,
                        scoring = scoring,
                        refit = 'neg_root_mean_squared_error')

grid_kn.fit(X_train, y_train)
print(grid_kn.best_score_)
print(grid_kn.best_params_)
    


# %%
print(grid_kn.best_score_)
print(grid_kn.best_params_)

# %%
# AdaBoost

kn = AdaBoostRegressor()
# params = {'n_estimators':[1000], 'base_estimator':DecisionTreeRegressor(max_depth=range(2, 11))}
params = {'n_estimators':[1000], 'base_estimator':[2]}

list = ['r2','neg_mean_squared_error','neg_root_mean_squared_error']


for i in list:
    grid_kn = GridSearchCV(estimator = kn,
                            param_grid = params,
                            cv = 5,
                            scoring = i,
                          error_score='raise')

    grid_kn.fit(X_train, y_train)
    print(grid_kn.best_score_)
    print(grid_kn.best_params_)
    


# %%
import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns

print('Pandas version:', pd.__version__)
# Pandas version: 1.3.0

tips = sns.load_dataset("tips")

tips["total_bill_cut"] = pd.cut(tips["total_bill"],
                                np.arange(0, 55, 5),
                                include_lowest=True,
                                right=False)

def cramers_v(confusion_matrix):
    """ calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher,
        Journal of the Korean Statistical Society 42 (2013): 323-328
    """
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    
    print(ss.chi2_contingency(confusion_matrix))


    print(chi2)
    n = confusion_matrix.sum()
    print(n)
    phi2 = chi2 / n
    print(phi2)
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

confusion_matrix = pd.crosstab(tips["day"], tips["time"])
cramers_v(confusion_matrix.values)
print(confusion_matrix)

# Out[2]: 0.9386619340722221

confusion_matrix = pd.crosstab(tips["total_bill_cut"], tips["time"])
cramers_v(confusion_matrix.values)
# Out[3]: 0.1649870749498837

tips

# %%





