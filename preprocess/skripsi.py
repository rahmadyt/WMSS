'''
Created on 14 Jul 2017

@author: USER
'''
#bigram untuk file sqlite, *SELESAI*
import re
import nltk
import jellyfish as jf
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())
file = open(r"C:\Users\USER\Desktop\big.txt", "r", encoding="utf-8-sig") #jgn lupa hapus tanda baca dll
# file = re.sub('[^a-zA-Z0-9#@]+', ' ', str(file))
bigrams = [b for l in file for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
file = open(r"C:\Users\USER\Desktop\big.txt", "r", encoding="utf-8-sig")
# file = re.sub('[^a-zA-Z0-9#@]+', ' ', str(file))
freq = nltk.FreqDist(bigrams) #computes freq of occurrence
fdist = freq.keys() # sorted according to freq

WORDS = Counter(bigrams)
WORDS1 = Counter(file.read().split())
#wordfreq = []
#for w in WORDS1:
    #wordfreq.append(WORDS1)
    #wordfreq[w]
    #print(wordfreq[w])

#bayes
def P(line): #N=sum(WORDS.values())
    "Probability of `word`."
    words = line.split()
    w1 = words[0]
    w2 = words[1]
    #print(wordfreq[w1])
    return WORDS[(w1, w2)]/WORDS1[w1]

#edit distance
def bigram_corr(line): #function with input line(sentence)
    words = line.split() #split line into words
    for idx, (word1, word2) in enumerate(zip(words[:-1], words[1:])):
#     line = list(itertools.chain.from_iterable(line))
        for i,j in fdist: #iterate over bigrams
            if (word2==j) and (jf.levenshtein_distance(word1,i) < 5): #if 2nd words of both match, and 1st word is at an edit distance of 2 or 1, replace word with highest occurring bigram
                idx = 0
                words[idx] = i
            elif (word1==i) and (jf.levenshtein_distance(word2,j) < 5):
                idx = 1
                words[idx] = j
    return " ".join(words)

def candidate(line):
    return ([bigram_corr(line)] or [line])

def bigram_corr2(line):
    try:
        return max([bigram_corr(line)], key=P)
    except ZeroDivisionError:
        return line

def bigram_corr3(line): #satu kalimat
    line = line.strip()
    line = " ".join(line.split())
    bigrams1 = re.sub('[^a-zA-Z0-9#@]+', ' ', line)
    bigrams1 = [b for b in zip(line.split(" ")[:-1], line.split(" ")[1:])]
#     print(bigrams1)
    hasil=[]
    for index, line in enumerate(bigrams1):
        if index == 0:
            hasil = bigram_corr2(' '.join(line)).split(' ')
#             hasil = bigram_corr2(' '.join(line))
        else:
            hasil.append(bigram_corr2(' '.join(line)).split(' ')[1])
#             hasil.append(bigram_corr2(' '.join(line))[1])
    return ' '.join(hasil)
#     return hasil

def bigram_corr4():
    import sqlite3

    f = sqlite3.connect("C:/Users/USER/Desktop/Tingkat 4/Skripsi/final.sqlite")
    cursor = f.cursor()

    #create table
    #cursor.execute('''CREATE TABLE TWEETS
    #(ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #NAME           TEXT    NOT NULL,
    #TWEET          TEXT    NOT NULL);''')

    #read
    a = cursor.execute("SELECT TWEET from TWEETS")
    tweet = []
    for row in a:
#     print(row)
        tweet.append(row[0])
#     hasil=[]
    #delete
    #a= cursor.execute("DELETE from TWEETS")
    #f.commit()
    
    f.close()
    
    hasil=[]
    for line in tweet:
#         line.rstrip()
        hasil.append(bigram_corr3(line))
#         print(hasil)
    #return ''.join(str(hasil))
    return hasil



#print(bigram_corr4()) #penyelesaian untuk kata yang tidak ada di corpus
for a in bigram_corr4():
    print(a)
