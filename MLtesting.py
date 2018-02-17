from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


data = pd.read_csv('masterPitchDataFrame.csv', sep='\s+', names = ['index','chorus_num','year','rank','pitches'])
#data = data[:10000]
print data.head(4)
chorus_num = list(data.chorus_num)
rank = list(data.rank)
year = list(data.year)
pitches = list(data.pitches)



scaler = StandardScaler()
# Don't cheat - fit only on training data
scaler.fit(X_train)
X_train = scaler.transform(X_train)
# apply same transformation to test data
X_test = scaler.transform(X_test)



#cross_val_score(model,x,y,cv=10,scoring = 'roc_auc')
score = cross_val_score(model,x,y,cv=10, scoring = 'accuracy')
score = np.mean(cross_val_score(model,x,y,cv=10))
return model, score

'''

#models and where they're from
def models():
    clf1 = LogisticRegression() #linear_model
    clf2 = RandomForestClassifier() #ensemble
    clf3 = GaussianNB() #naive bayes
    eclf = VotingClassifier(estimators=[('lf',clf1),('rf',clf2),('gnb',clf3)],voting = 'hard') #ensemble
    #hard = majority rule, gives you class soft = unknown. different probabilities
    return clf1, clf2, clf3, eclf

#place models into a list so we can test each one of them
clf1, clf2, clf3, eclf = models()
classifiers = [clf1, clf2, clf3, eclf]

print (x.shape)
print (y.shape)
for model in classifiers:
    #cross_val_score(model,x,y,cv=10,scoring = 'roc_auc')
    score = cross_val_score(model,x,y,cv=10, scoring = 'accuracy')
    score = np.mean(cross_val_score(model,x,y,cv=10))
return model, score
'''
