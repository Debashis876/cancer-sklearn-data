import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.datasets import load_breast_cancer
cancer_dataset = load_breast_cancer()
cancer_dataset.keys()
cancer_dataset['data']
cancer_dataset['target_names']
print(cancer_dataset['DESCR'])
print(cancer_dataset['feature_names'])
cancer_df = pd.DataFrame(np.c_[cancer_dataset['data'],cancer_dataset['target']],columns = np.append(cancer_dataset['feature_names'], ['target']))
cancer_df.head(6)
cancer_df.info()
# create second DataFrame by droping target
cancer_df2 = cancer_df.drop(['target'], axis = 1)
print("The shape of 'cancer_df2' is : ", cancer_df2.shape)
plt.figure(figsize = (16,5))
ax = sns.barplot(cancer_df2.corrwith(cancer_df.target).index, cancer_df2.corrwith(cancer_df.target))
ax.tick_params(labelrotation = 90)
X = cancer_df.drop(['target'], axis = 1)
X.head(6)
y = cancer_df['target']
y.head(6)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state= 5)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_sc = sc.fit_transform(X_train)
X_test_sc = sc.transform(X_test)
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

from xgboost import XGBClassifier
xgb_classifier2 = XGBClassifier()
xgb_classifier2.fit(X_train_sc, y_train)
y_pred_xgb_sc = xgb_classifier2.predict(X_test_sc)
accuracy_score(y_test, y_pred_xgb_sc)

from xgboost import XGBClassifier
xgb_classifier = XGBClassifier()
xgb_classifier.fit(X_train, y_train)
y_pred_xgb = xgb_classifier.predict(X_test)
accuracy_score(y_test, y_pred_xgb)

params={
 "learning_rate"    : [0.05, 0.10, 0.15, 0.20, 0.25, 0.30 ] ,
 "max_depth"        : [ 3, 4, 5, 6, 8, 10, 12, 15],
 "min_child_weight" : [ 1, 3, 5, 7 ],
 "gamma"            : [ 0.0, 0.1, 0.2 , 0.3, 0.4 ],
 "colsample_bytree" : [ 0.3, 0.4, 0.5 , 0.7 ] 
}

from sklearn.model_selection import RandomizedSearchCV
random_search = RandomizedSearchCV(xgb_classifier, param_distributions=params, scoring= 'roc_auc', n_jobs= -1, verbose= 3)
random_search.fit(X_train, y_train)

random_search.best_params_

random_search.best_estimator_


xgb_classifier_pt = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bynode=1, colsample_bytree=0.4, gamma=0.2,
       learning_rate=0.1, max_delta_step=0, max_depth=15,
       min_child_weight=1, missing=None, n_estimators=100, n_jobs=1,
       nthread=None, objective='binary:logistic', random_state=0,
       reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
       silent=None, subsample=1, verbosity=1)
 
xgb_classifier_pt.fit(X_train, y_train)


y_pred_xgb_pt = xgb_classifier_pt.predict(X_test)

accuracy_score(y_test, y_pred_xgb_pt)

print(classification_report(y_test, y_pred_xgb_pt))
pickle.dump(xgb_classifier_pt, open('model.pkl', 'wb'))


breast_cancer_detector_model = pickle.load( open('model.pkl', 'rb'))

y_pred = breast_cancer_detector_model.predict(X_test)

print('Confusion matrix of XGBoost model: \n',confusion_matrix(y_test, y_pred),'\n')

print('Accuracy of XGBoost model = ',accuracy_score(y_test, y_pred))
