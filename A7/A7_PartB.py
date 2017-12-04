
# coding: utf-8

# In[2]:

"""
Aman Arya
CSE 415
1535134
A7: Part B
Fake News Classification via Naive Bayes and LSA
"""
#get_ipython().magic(u'matplotlib inline')
import itertools
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans


# In[3]:

# Import `fake_or_real_news.csv` 
df = pd.read_csv("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/fake_or_real_news.csv")


# In[4]:

df.shape


# In[5]:

df.head()


# In[6]:

df = df.set_index("Unnamed: 0") 
df.head()


# In[7]:

y = df.label 
df.drop("label", axis=1)
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)


# In[8]:

# Initialize the `tfidf_vectorizer` 
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.4, min_df=2, use_idf=True, norm='l2') 

# Fit and transform the training data 
tfidf_train = tfidf_vectorizer.fit_transform(X_train) 

# Transform the test set 
tfidf_test = tfidf_vectorizer.transform(X_test)


# In[9]:

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
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


# In[10]:

clf = MultinomialNB()


# In[11]:

clf.fit(tfidf_train, y_train)
pred = clf.predict(tfidf_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])


# In[ ]:

lsa = TruncatedSVD(n_components=100)


# In[ ]:

X = lsa.fit_transform(tfidf_train)
print("LSA fit and transformed")


# In[ ]:
km = KMeans(n_clusters=2, init='k-means++', algorithm='full')
km.fit(tfidf_train)
pred_km = km.predict(tfidf_test)
print("First predictions")
print(pred_km[0:5])
lookup_table = np.array(['REAL', 'FAKE'])
pred_km = lookup_table[pred_km]
print(pred_km[0:5])

score = metrics.accuracy_score(y_test, pred_km)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(y_test, pred_km, labels=['FAKE', 'REAL'])
plot_confusion_matrix(cm, classes=['FAKE', 'REAL'])