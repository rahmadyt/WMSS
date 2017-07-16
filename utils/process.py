from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from nltk.tokenize import WhitespaceTokenizer
from sklearn import metrics
from sklearn.svm import LinearSVC
import numpy as np
import pickle
import re
import os

model_path = os.path.join(os.path.dirname(__file__), 'model')
dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
vocab_path = os.path.join(model_path, 'vocab')

def regex_when(berita):
    when_word_list = set(map(lambda x: x.strip('\n') , open(os.path.join(dataset_path, 'kapan_list.txt'), 'r').readlines()))
    expression = re.compile(
        '(' +
        '|'.join(re.escape(item) for item in when_word_list) +
        '|\(\d+\/\d+\/\d+\)' +
        '|\(\d+\/\d+\)' +
        '|(\d{1,2}.\d{2})'
        ')')
    
    when_index = list()
    
    for index, kalimat in enumerate(berita):
        if expression.search(kalimat.lower()):
            when_index.append(index)
    
    return [berita[index] for index in when_index]

def f4_weight(list_sentences):
    f4 = list();
    for index, sentence in enumerate(list_sentences):
        other_sentences = [item for sublist in (list_sentences[:index]+list_sentences[index+1:]) for item in sublist]
        intercept = set(sentence).intersection(other_sentences)
        union = set(sentence).union(other_sentences)
        f4.append(len(intercept) / float(len(union)))
    
    return f4

def f5_weight( list_sentences, title ):
    f5 = list()
    for sentence in list_sentences:
        f5.append(len(set(title).intersection(sentence)) / float(len(set(title).union(sentence))))
    return f5

def f2_weight(list_sentences):
    f2 = list()
    corpus = pickle.load(open(os.path.join(model_path, 'corpus_token.p'), "rb" ))
    corpus_len = len(corpus)
    
    sentences_len = len(list_sentences)
    
    for sentence in list_sentences:
        #panjang setiap kalimat
        sentence_len = len(sentence)
        if(sentence_len == 0):
            continue
        f2_temp = 0
        for token in set(sentence):
            tfi = sentence.count(token)
            sentence_that_contain_word = len(list(filter(lambda sent: token in sent, list_sentences)))
            corpus_that_contain_word = len(list(filter(lambda sent: token in sent, corpus)))
            pkss = sentence_that_contain_word/len(list_sentences)
            pss = sentences_len/corpus_len
            if(corpus_that_contain_word == 0):
                continue
            else:
                pk = corpus_that_contain_word/corpus_len
                f2_temp += tfi*((pkss*pss)/pk)
        f2.append(f2_temp/sentence_len)
        
    return f2

def bow(list_sentences, vocab = 'all'):
    if vocab not in ['all', 'f4', 'f5', 'sum']:
        print('error')
        return
    
    vocab = pickle.load(open(os.path.join(vocab_path, vocab+"_bow_vocab.p"), "rb" ))
    count_vectorizer = CountVectorizer(analyzer = "word", vocabulary=vocab)
    return count_vectorizer.fit_transform([' '.join(sentence) for sentence in list_sentences]).toarray()

def tfidf(list_sentences, vocab = 'all'):
    if vocab not in ['all', 'f4', 'f5', 'sum']:
        print('error')
        return
    
    vocab = pickle.load(open(os.path.join(vocab_path, vocab+"_tfidf_vocab.p"), "rb" ))
    tfidf_vectorizer = TfidfVectorizer(analyzer = "word", vocabulary=vocab)
    return tfidf_vectorizer.fit_transform([' '.join(sentence) for sentence in list_sentences]).toarray()

def predict(berita, f2=list(), f4=list(), f5=list()):
    if(len(f2)<=0):
        f2=f2_weight(berita['token_isi'])
    if(len(f4)<=0):
        f4=f4_weight(berita['token_isi'])
    if(len(f5)<=0):
        f5=f5_weight(berita['token_isi'], berita['token_judul'])
    
    weight = list(map(lambda f2, f4, f5: [f2*30, f4*39, f5*49], f2, f4, f5))
    feature = list(map(lambda t, b, w: np.append(np.append(t, b), w), tfidf(berita['token_isi']), bow(berita['token_isi']), weight))
    clf = pickle.load(open(os.path.join(model_path, "all_btw_model.p"), "rb" ))
    code_prediction = clf.predict(feature)
    
    prediction = {'apa': list(), 'dimana': list(), 'bagaimana': list(), 'kapan': list(), 'siapa': list(), 'mengapa': list()}
    for index, p in enumerate(code_prediction):
        if(p[0]):
            prediction['apa'].append(berita['list_isi'][index])
        if(p[1]):
            prediction['dimana'].append(berita['list_isi'][index])
        if(p[2]):
            prediction['bagaimana'].append(berita['list_isi'][index])
        if(p[3]):
            prediction['kapan'].append(berita['list_isi'][index])
        if(p[4]):
            prediction['siapa'].append(berita['list_isi'][index])
        if(p[5]):
            prediction['mengapa'].append(berita['list_isi'][index])
    
    return prediction