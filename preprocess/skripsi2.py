'''
Created on 14 Jul 2017

@author: USER
'''
#Cek typo per kata - ED + Bayes
import re
import os
from collections import Counter
import sqlite3


def words(text): return re.findall(r'\w+', text.lower())
# path = 'C:/Users/USER/Desktop/Parallel Corpus'

# for filename in os.listdir(path):
BASE_DIR = os.path.dirname((__file__))
file = os.path.join(BASE_DIR, 'big.txt')
file = open(file, "r", encoding="utf-8-sig") #jgn lupa corpus di bikin lower text; buat fungsi
WORDS = Counter(file.read().split())

def rules(word):
    pjg = len(word)
    typo=[]
    if pjg == 1:
        if re.search(r"([a-zA-Z])", word) :
            typo.append(word)
    elif pjg == 2:
        if re.search(r"([a-zA-Z]+[a-zA-Z])", word) :
            typo.append(word)
    elif pjg > 2 :
        vocal = re.search(r"([a]+[i]|[a]+[u]|[e]+[i]|[o]+[i]|[k]+[h]|[n]+[g]|[n]+[y]|[s]+[y])", word)
#         cons = re.search(r"([k]+[h]|[n]+[g]|[n]+[y]|[s]+[y])", word)
        if not vocal:
            typo.append(word)
#         else :
#             typo.append(word)
#     elif re.search(r"([a-zA-Z]+[a-zA-Z]+[a-zA-Z]+[a-zA-Z])", word) :
#             typo.append(word)
    return typo
    
def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): #untuk kata
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correction_2(lines): #untuk kalimat ED + Bayes
    separate=[]
    separate.append(lines.split())
    for line in separate:
        hasil=[]
        for word in line:
            hasil.append(correction(word))
        return ' '.join(hasil)

def correction_3(lines): #untuk kalimat Rule, ED + Bayes
    lines = lines.strip()
    lines = " ".join(lines.split())
    lines = re.sub('[^a-zA-Z0-9#@]+', ' ', lines)
    separate=[]
    separate.append(lines.split())
    for line in separate:
        hasil=[]
        for word in line:
#             rules(word)
            if word in rules(word):
                hasil.append(correction(word))
            else:
                hasil.append(word)
        return ' '.join(hasil)           
    
def bigram_corr5(tweet):
       
    hasil=[]
#     print(tweet)
    for line in tweet:
        hasil.append(correction_3(line))
    return hasil
#     return ' '.join(hasil)


# print(correction_3('jasaa menyebutka terdaka juga memperkayaa'))
# print(correction_2('jasaa menyebutka terdaka juga memperkayaa'))
# candidates('Kementriann')
# print(WORDS)
# rules('khusus')