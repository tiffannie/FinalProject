
# coding: utf-8

# In[2]:

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import  MLPRegressor
import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


# In[6]:

data = pd.read_pickle('masterPitchDataFrame.pkl')

print data.head(4)
print data.shape


# In[15]:

from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# In[62]:

from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
data['chorus_num_code'] = encoder.fit_transform(data['chorus_num'])
#print data[['chorus_num',"chorus_num_code"]].head()

data['year_code'] = encoder.fit_transform(data['year'])
#print data[['year',"year_code"]].head(200)


# In[65]:

columns = data.columns.tolist()
columns = [c for c in columns if c not in ["rank","chorus_num","year"]]
print data.columns

y = data["rank"]#.astype(float)
x = data[columns]#.astype(float)
#print x
seed = 7


# In[17]:

# prepare models
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))


# In[66]:

print type(target)
# evaluate each model in turn
data = data.reindex()
results = []
names = []
scoring = 'accuracy'
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, x, y, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


# In[68]:

import matplotlib.pyplot as plt
# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

