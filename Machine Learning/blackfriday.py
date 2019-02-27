import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# read in data
friday = pd.read_csv('BlackFriday.csv')

# functions
def fix_age(cols):
    Age = cols[0]
    if Age == '55+':
        return Age.split('+')[0]
    else:
        return Age.split('-')[1]
def fix_years(cols):
    Years = cols[0]
    if Years == '4+':
        return Years.split('+')[0]
    else:
        return Years
def number_city(cols):
    City = cols[0]
    if City == 'A':
        return 1
    elif City == 'B':
        return 2
    else:
        return 3

# clean data
friday.drop('Product_Category_3',axis=1,inplace=True)
friday.drop('Product_Category_2',axis=1,inplace=True)
friday.dropna(inplace=True)
sex = pd.get_dummies(friday['Gender'],drop_first=True)
friday.drop('Product_ID',axis=1,inplace=True)
friday = pd.concat([friday,sex],axis=1)
friday['Age'] = friday[['Age']].apply(fix_age,axis=1)
friday['Stay_In_Current_City_Years'] = friday[['Stay_In_Current_City_Years']].apply(fix_years,axis=1)
friday.drop('Gender',axis=1,inplace=True)
friday['City_Category'] = friday[['City_Category']].apply(number_city,axis=1)

# ML
friday_frac = friday.sample(frac=0.02)
X = friday_frac.drop('M',axis=1)
y = friday_frac['M']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.30)

# scale data
scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# gridsearch
param_grid = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
grid = GridSearchCV(SVC(),param_grid,verbose=3)
grid.fit(X_train_scaled,y_train)
grid_predictions = grid.predict(X_test_scaled)

# print accuracy
print(confusion_matrix(y_test,grid_predictions),'\n')
print(classification_report(y_test,grid_predictions))
