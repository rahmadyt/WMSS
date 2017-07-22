# from sklearn.feature_extraction.text import TfidfTransformer
# from keras.models import model_from_json
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.tokenize import word_tokenize
# from textblob import TextBlob as tb
# import pickle
# import tensorflow as tf
# 
# stopWordIndo = word_tokenize(open('E:/StopWord.txt',encoding="utf8").read()) #stopwordremoval
# stemmer = StemmerFactory().create_stemmer() #sastrawistemming
# X_Test = [] #main clean dataset
# def inputPrepros(f):
#     bucket = []
#     word_tokens = word_tokenize(f)
#     for i in word_tokens: #stop word removal
#         if i not in stopWordIndo:
#             bucket.append(i)
#     doc = str(tb(' '.join(bucket)))
#     X_Test.append(stemmer.stem(doc)) #stemming
#     return stemmer.stem(doc)
# 
# #Feature Extraction Options
# #TF
# def tf(i):
#     vectorizer = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_tf_vocab.pkl", "rb")))
#     freq_term_matrix = vectorizer.transform(X_Test).todense()
#     if (i == 0) :
#         return freq_term_matrix
#     else :
#         return len(vectorizer.vocabulary_)
#     
# #TF-IDF
# def tf_idf(i):
#     freq_term_matrix = tf(0)
#     #IDF
#     tfidf = TfidfTransformer(norm="l2")
#     tfidf.fit(freq_term_matrix)
#     #TF-IDF
#     tf_idf_matrix = tfidf.transform(freq_term_matrix)
#     TF_IDF = tf_idf_matrix.todense()
#     if (i == 0) :
#         return TF_IDF
#     else :
#         return tf(1)
#     
# #BAG OF WORD
# def bow(i):
#     vectorizer = CountVectorizer(binary=True,decode_error="replace",vocabulary=pickle.load(open("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_bow_vocab.pkl", "rb")))
#     bOw = vectorizer.transform(X_Test).todense()
#     if (i == 0) :
#         return bOw
#     else :
#         return len(vectorizer.vocabulary_)
# 
# #N GRAM
# def nGram(i):
#     vectorizer = CountVectorizer(ngram_range=(2,2),decode_error="replace",vocabulary=pickle.load(open("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_nGram_vocab.pkl", "rb")))
#     nGram = vectorizer.transform(X_Test).todense()
#     if (i == 0) :
#         return nGram
#     else :
#         return len(vectorizer.vocabulary_)
# 
# 
# # load the model from disk
# def modelVector(f,opsi):
#     if (opsi==1): #TF
#         json_file = open('E:/Projek/WMSS/dlnn/Model_Used/DLNN2_tf_model.json', 'r')
#         loaded_model_json = json_file.read()
#         loaded_model = model_from_json(loaded_model_json)
#         X_Test = tf(0)
#         modelWeight = loaded_model.load_weights("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_tf_weight.h5") 
#     elif(opsi==2): #TF-IDF
#         json_file = open('E:/Projek/WMSS/dlnn/Model_Used/DLNN2_tfIdf_model.json', 'r')
#         loaded_model_json = json_file.read()
#         loaded_model = model_from_json(loaded_model_json) 
#         X_Test = tf_idf(0)
#         modelWeight = loaded_model.load_weights("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_tfIdf_weight.h5")
#     elif(opsi==3): #BagOfWord
#         json_file = open('E:/Projek/WMSS/dlnn/Model_Used/DLLN2_bow_model.json', 'r')
#         loaded_model_json = json_file.read()
#         loaded_model = model_from_json(loaded_model_json) 
#         X_Test = bow(0)
#         modelWeight = loaded_model.load_weights("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_bow_weight.h5")
#     else: #Bigram 
#         json_file = open('E:/Projek/WMSS/dlnn/Model_Used/DLNN2_nGram_model.json', 'r')
#         loaded_model_json = json_file.read()
#         loaded_model = model_from_json(loaded_model_json) 
#         X_Test = nGram(0)
#         modelWeight = loaded_model.load_weights("E:/Projek/WMSS/dlnn/Model_Used/DLNN2_nGram_weight.h5")
#     return X_Test,loaded_model,modelWeight
#     
# def gabungdata(f,opsi):
#     print(inputPrepros(f))
#     X_FinalTest, loaded_model , modelWeight = modelVector(X_Test,opsi)
#     #X_FinalTest = loaded_vec.transform(X_Test).todense()
#     print(X_FinalTest[len(X_FinalTest)-1])
#     
#     result = loaded_model.predict(X_FinalTest)
#     print(result[len(result)-1])
#     if(result[len(result)-1]>[0.5]):
#         return "=> Sentimen Positif"
#     else:
#         return "=> Sentimen Negatif"