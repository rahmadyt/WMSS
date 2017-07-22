from django.test import TestCase
import os
import re
import json
import sqlite3
# Create your tests here.

BASE_DIR = os.path.dirname((__file__))
var = os.path.join(BASE_DIR, 'var.txt')

def readfile(a):
    f = open(a,'r')
    c = f.read(1)
    f.close
    return c

class usedvar:
    abc = readfile(var)
    method = abc
    
def handle_uploaded_file(f, g):
    ##Jika ingin menyimpan dalam folder yang berbeda
    #filename, fileext = os.path.splitext(g)
    #g = "Media/"+fileext[1:]+"/"+g
#statis langsung
    g = "static/tables/"+g
    g = os.path.join(BASE_DIR, g)
    with open(g, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def getFile():
    ##jika ingin menggunakan media
    #json = os.path.join(BASE_DIR, "Media/JSON")
    #CommaSV = os.path.join(BASE_DIR, "Media/CSV")
    #a = os.listdir(json)
    #b = os.listdir(CommaSV)
#static langsung
    a = []
    b = []
    p = os.path.join(BASE_DIR,'static/tables/')
    data = os.listdir(p)
    for da in data:
        nama, ext = os.path.splitext(da) 
        if ext.lower()==".json":
            a.append(da)
        elif ext.lower()==".csv":
            b.append(da)
    return a,b

def getFilename():
    json, commasv = getFile()
    listnamaJSON = []
    listnamaCSV = []
    for a in json:
        a,b = os.path.splitext(a)
        listnamaJSON.append(a)
    for a in commasv:
        a,b = os.path.splitext(a)
        listnamaCSV.append(a)
    return listnamaJSON, listnamaCSV

def getKeyJson(data):
    p = os.path.join(BASE_DIR,'static/tables/')
    f = open(p+data, 'r', encoding='utf-8')
    g = json.load(f)
    c ={}
    b =[]
    for a in g:
        for key in a.keys():
            c[key]=''
    for key in c.keys():
        b.append(key)
    return b

def uploadtoarray(data):
    a = []
    for chunk in data.chunks():
        a.append(chunk)  
    return a

def getall():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_temp = os.path.join(BASE_DIR, 'db.sqlite3')
    
    conn = sqlite3.connect(db_temp)
    cursor = conn.cursor()
    a = cursor.execute("SELECT NAME, TWEET, RETWEET_USER, HASHTAG from WMMS_TwitterCrawl")
    c = {'users':[],'twits':[],'ritwistUsr':[],'ritwits':[],'hashtags':[]}
    for row in a:
        c['users'].append(row[0])
        c['twits'].append(row[1])
        c['ritwits'].append(row[2])
        c['hashtags'].append(row[3])
    return c
