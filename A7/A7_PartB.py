
# coding: utf-8

# In[2]:

"""
Aman Arya
CSE 415
1535134
A7: Part B
Fake News Classification via Naive Bayes and LSA
"""
import itertools
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier


# In[3]:

# Import `fake_or_real_news.csv` 
df = pd.read_csv("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/fake_or_real_news.csv")


# In[6]:

df = df.set_index("Unnamed: 0") 
df.head()


# In[7]:

y = df.label 
df.drop("label", axis=1)
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)


# In[8]:

# Initialize the `tfidf_vectorizer` 
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.6, min_df=3, use_idf=True, norm='l2', sublinear_tf=True, ngram_range=(1, 2)) 

# Fit and transform the training data 
tfidf_train = tfidf_vectorizer.fit_transform(X_train) 

# Transform the test set 
tfidf_test = tfidf_vectorizer.transform(X_test)


# In[9]:

def plot_confusion_matrix(cm, classes, name,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.clf()
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(name)


# In[10]:
clf = LogisticRegression(penalty="l2")

clf.fit(tfidf_train, y_train)
pred = clf.predict(tfidf_test)
print "Logistic Regression F1 and Accuracy Scores : \n"
print ( "F1 score {:.4}%".format( metrics.f1_score(y_test, pred, average='macro')*100 ) )
print ( "Accuracy score {:.4}%".format(metrics.accuracy_score(y_test, pred)*100) )
cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'], name="LogReg.png")

# In[11]:
scores = cross_val_score(clf, tfidf_train, y_train, cv=5)
print(scores)


# In[12]:

lsa = TruncatedSVD(n_components=100, n_iter=10)


# In[13]:

X = lsa.fit_transform(tfidf_train)
t = lsa.transform(tfidf_test)
print("LSA fit and transformed")


# In[14]:
knn = KNeighborsClassifier(n_neighbors=5, metric='minkowski')
knn.fit(X, y_train)

# In[15]:
pred_km = knn.predict(t)

# In[15]
print "LSA + KNN F1 and Accuracy Scores : \n"
print ( "F1 score {:.4}%".format( metrics.f1_score(y_test, pred_km, average='macro')*100 ) )
print ( "Accuracy score {:.4}%".format(metrics.accuracy_score(y_test, pred_km)*100) )
cm = metrics.confusion_matrix(y_test, pred_km, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'], name="LSA.png")

scores = cross_val_score(knn, X, y_train, cv=5)
print(scores)

#In[16]
feat_names = tfidf_vectorizer.get_feature_names()

for compNum in range(0, 2):
    plt.clf()
    comp = lsa.components_[compNum]
    
    indeces = np.argsort(comp).tolist()
    
    indeces.reverse()
    
    terms = [feat_names[weightIndex] for weightIndex in indeces[0:10]]    
    weights = [comp[weightIndex] for weightIndex in indeces[0:10]]    

    terms.reverse()
    weights.reverse()
    positions = np.arange(10) + .5    
    
    plt.figure(compNum)
    plt.barh(positions, weights, align='center')
    plt.yticks(positions, terms)
    plt.xlabel('Weight')
    plt.title('Strongest terms for component %d' % (compNum))
    plt.grid(True)
    plt.show()