import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.cluster import KMeans

# read in data
colleges = pd.read_csv('College_Data',index_col=0)

# initialize model
kmeans = KMeans(n_clusters=2)

# fit to data
kmeans.fit(colleges.drop('Private',axis=1))

# function on cluster
def converter(cluster):
    if cluster=='Yes':
        return 1
    else:
        return 0

# clean data
# colleges['Grad.Rate']['Cazenovia College'] = 100
colleges['Cluster'] = colleges['Private'].apply(converter)
colleges.drop('Private',axis=1,inplace=True)

# visualization
sns.set_style('darkgrid')
g = sns.FacetGrid(colleges,hue="Cluster",palette='coolwarm',height=6,aspect=2)
g = g.map(plt.hist,'Grad.Rate',bins=20,alpha=0.7)
plt.show()

# print accuracy
# print(confusion_matrix(colleges['Cluster'],kmeans.labels_))
# print(classification_report(colleges['Cluster'],kmeans.labels_))
