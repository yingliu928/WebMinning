# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings("ignore")
label = LabelEncoder()


def stopwords_removal(corpus):
    wh_words = ['who', 'what', 'when', 'why', 'how', 'which', 'where', 'whom']
    stop = set(stopwords.words('english'))
    for word in wh_words:
        stop.remove(word)
    corpus = [[x for x in x.split() if x not in stop] for x in corpus]
    return corpus


def lemmatize(corpus):
    lem = WordNetLemmatizer()
    corpus = [[lem.lemmatize(x, pos='v') for x in x] for x in corpus]
    return corpus


def stem(corpus, stem_type=None):
    stemmer = PorterStemmer()
    corpus = [[stemmer.stem(x) for x in x] for x in corpus]
    return corpus


def preprocess(corpus):
    corpus = stopwords_removal(corpus)
    corpus = lemmatize(corpus)
    corpus = stem(corpus)
    corpus = [' '.join(x) for x in corpus]
    return corpus


def load_data(filename):
    print('open file {}'.format(filename))
    df = pd.read_csv(filename)
    df.rename(columns={df.columns[0]: "description",
              df.columns[1]: "position"}, inplace=True)
    df.drop(df.columns.difference(
        ['position', 'description']), 1, inplace=True)
    df.dropna(subset=['position', 'description'])

    # df_new = df.loc[df['position'].isin(
    #     ['Data Scientist', 'Software Engineer'])]
    # print(df_new)

    X_train, X_test, y_train, y_test = train_test_split(
        df.description, df.position, test_size=0.2)
    return X_train, X_test, y_train, y_test


def train_model(X_train, X_test, y_train, y_test):
    # encode 'Data Scientist', 'Software Engineers' into 0 or 1
    # label = LabelEncoder()
    y_train_enc = label.fit_transform(y_train)
    y_test_enc = label.fit_transform(y_test)

    # instantiate term frequency–inverse document frequency
    vect = TfidfVectorizer()

    # # use it to extract features from training data. It returns the document-term matrix
    X_train_dtm = vect.fit_transform(X_train)

    # transform testing data (using training data's features)
    X_test_dtm = vect.transform(X_test)

    # # instantiate a Support Vector Classifier
    classifier = SVC(kernel='linear')

    # fit the model with training data
    classifier.fit(X_train_dtm, y_train_enc)

    # # Make predictions on test data
    y_pred_class = classifier.predict(X_test_dtm)

    # # calculate evaluation measures:
    print("Accuracy: ", accuracy_score(y_test_enc, y_pred_class))
    return classifier, vect


def run(X_train, X_test, y_train, y_test):
    X_train = preprocess(X_train)
    X_test = preprocess(X_test)
    classifier, vect = train_model(X_train, X_test, y_train, y_test)
    return classifier, vect


def load_data_test(filename, classifier, vect):
    print('open file {}'.format(filename))
    df = pd.read_csv(filename)
    X_test = preprocess(df.columns[0])
    X_test_dtm = vect.transform(X_test)
    y_pred_class = classifier.predict(X_test_dtm)
    predictions_test = label.inverse_transform(y_pred_class)
    # print(predictions_test)
    df['position'] = pd.DataFrame(predictions_test)
    # print(df)
    print('Complete prediction. Generated file in ./data/indeed_prediction.csv')
    df.to_csv('./data/indeed_prediction.csv', index=False)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_data(
        filename='./data/alldata.csv')
    run(X_train, X_test, y_train, y_test)
