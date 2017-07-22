from django.shortcuts import render, render_to_response
from social_media_crawling import scrape1, scrape2
from . import trends
from .models import TwitterCrawl, FacebookCrawl
from django.http.response import HttpResponseRedirect
from social_media_crawling.form import browse_id, advOpt, option, ScrapeOpt, upFile, fixbrowse, fixscrape
from .tests import usedvar, handle_uploaded_file, getFile, getKeyJson, uploadtoarray, getall
from social_media_crawling.bongbong import mainTotm
import os
from social_media_crawling import urls
import sqlite3
import json

# Create your views here.

def delet(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_temp = os.path.join(BASE_DIR, 'db.sqlite3')
    
    conn = sqlite3.connect(db_temp)
    cursor = conn.cursor()
    cursor.execute("DELETE from social_media_crawling_TwitterCrawl;")
    conn.commit()
    return HttpResponseRedirect('../search2')

def delet2(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_temp = os.path.join(BASE_DIR, 'db.sqlite3')
    
    conn = sqlite3.connect(db_temp)
    cursor = conn.cursor()
    cursor.execute("DELETE from social_media_crawling_FacebookCrawl;")
    conn.commit()
    return HttpResponseRedirect('../search2')

def changemetod(mth):
    BASE_DIR = os.path.dirname((__file__))
    var = os.path.join(BASE_DIR, 'var.txt')
    f = open(var,'w')
    f.write(mth)
    usedvar.method = mth
    f.close()

def index(request):
    return render(request, 'WMMS/index.html')


def crawl(request):
    #variabel
    m1 = request.session.get('Method')
    m2 = request.session.get('Lang')
    m3 = request.session.get('Tapdown')
    if m1==None:
        ad = usedvar.method
    else:
        ad = m1
    form1 = advOpt(request.POST)
    form = browse_id(request.POST)
    form2 = option(request.POST)
    form3 = ScrapeOpt(request.POST)
    #trend
    #countryL = trends.getCountry() #hapus commen jika siap pake
    #bad = trends.getAllTrending()
    
    #trend temp
    countryL = ['Worldwide','Indonesia','United Kingdom']
    bad = trends.getAllTrending(countryL)

    #form
    if request.method == 'POST':
        if 'methods' in request.POST:              
            if form1.is_valid():
                a = request.POST.get('methods')
                changemetod(a)
                request.session['Method']=form1.cleaned_data['methods']
                ad = form1.cleaned_data['methods']
            if form2.is_valid():
                request.session['Lang']=form2.cleaned_data['language']
                m2 = form2.cleaned_data['language']
            if form3.is_valid():
                request.session['Tapdown']=form3.cleaned_data['tapdown']
                m3 = form3.cleaned_data['tapdown']
                
        if 'crawl' in request.POST:
            if form.is_valid():
                data = request.POST.get('content')               
                if ad == '0':
                    scrape1.API(data,m2)
                if ad == '1':
                    scrape1.bac(data,m2,m3)
                
    return  render(request, 'WMMS/crawl.html', {
        'form': browse_id(), 'form1':advOpt(initial={'methods':ad}),'form2':option(initial={'language':m2}),'form3':ScrapeOpt(initial={'tapdown':m3}), 'country':countryL, 'm1':ad, 'test':bad, "f3":upFile
    })

def crawl2(request):
    #variabel
    twitterdata = TwitterCrawl.objects.all()
    facebookdata = FacebookCrawl.objects.all()
    m1 = request.session.get('Method')
    m2 = request.session.get('Lang')
    m3 = request.session.get('Tapdown')
    if m1==None:
        ad = usedvar.method
    else:
        ad = m1
    
    
    form2 = option(request.POST)
    form3 = ScrapeOpt(request.POST)
    #trend
    #countryL = trends.getCountry() #hapus commen jika siap pake
    #bad = trends.getAllTrending()
    
    #trend temp
#     countryL = ['Worldwide','Indonesia','United Kingdom']
#     bad = trends.getAllTrending(countryL)

    #form
    if request.method == 'POST':
        form = fixbrowse(request.POST)
        form1 = fixscrape(request.POST)
        form2 = upFile(request.POST, request.FILES)
        
        if 'API' in request.POST:              
            if form.is_valid():
                data = request.POST.get('content')
                bahasa = request.POST.get('language')
                scrape2.API(data,bahasa)
                                           
        if 'Scrape' in request.POST:
            if form.is_valid():
                data = request.POST.get('content') 
                bahasa = request.POST.get('language')    
                since = request.POST.get('since')
                until = request.POST.get('until')  
                tapdown = request.POST.get('tapdown')                     
                date = request.POST.get('date')
                date = [date,since,until]
                scrape2.scrapeTwitter(data,bahasa,int(tapdown),date)
            else:
                print(form.errors)
                
        if 'FScrape' in request.POST:
            data = request.POST.get('content')
            tapdown = request.POST.get('tapdown')
            scrape2.scrapeFacebook(data,int(tapdown))
                    
        if 'file' in request.FILES:           
            if form2.is_valid():
                handle_uploaded_file(request.FILES['file'],request.FILES['file'].name)
                print(request.FILES['file'].name)
            else:
                print(form.errors)  
                     
    d, e = getFile()
    listda ={}
    c =[]
    data = request.POST.get('data_choice')
    if data=='TWEETS' or data=='POSTS':
        data = None
    if data != None:
        listda[data] = getKeyJson(data)
        c = listda[data]
    
               
    return  render(request, 'WMMS/social_media_crawling.html', {
        'form': fixbrowse(), 'form1':fixscrape(initial={'date':'0','tapdown':'50'}), 'f3':upFile,'data' : c, 'test':d, 'test1':e, 'sta':data, 'Tweets':twitterdata, 'statuses':facebookdata
    })
    
def fileUpload(request):
    d, e = getFile()
    listda ={}
    c =[]
    data = request.POST.get('data_choice')
    if data != None:
        listda[data] = getKeyJson(data)
        c = listda[data]

    if request.method == 'POST':
        form = upFile(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],request.FILES['file'].name)
        else:
            print(form.errors)
        if 'TOTM' in request.POST:
            print('succes')
            datatwit = getall()
            mainTotm(datatwit)
            
    return render(request,'WMMS/test.html',{"f3":upFile, 'data' : c, 'test':d, 'test1':e, 'sta':data})

def analisis1(request):
    Cfeature = ['TF','TF-IDF','BOW','BIGRAM']
    algorthm = ['SVM','Deep learning', 'Naive bayes']
    hasil = "Sentimen Positif"
    
    if request.method == 'POST':
        form = upFile(request.POST, request.FILES)
        if form.is_valid():
            print(uploadtoarray(request.FILES['file']))
            print(request.POST.get('Cfeature'))
            print(request.POST.get('algorthm'))
        else:
            print(form.errors)
        
        
    return render(request,'WMMS/test1.html',{"f3":upFile, 'test':Cfeature, 'test1':algorthm, 'hasil':hasil})
