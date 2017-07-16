from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django. views.generic import TemplateView
from django.template.context_processors import request, csrf
import urllib.request
from bs4 import BeautifulSoup
import re
import sys, os, csv, io
from django.views.decorators.csrf import requires_csrf_token, csrf_protect
from django.template.defaulttags import csrf_token
from crawling.forms import *
from pip._vendor.requests.models import Request
from django.http.response import HttpResponseRedirect
import webbrowser
from django.core.urlresolvers import reverse
from crawling.models import Hasil_Pencarian_Keyword, Tabel_Berita
from .tests import *
from django.http.request import RAISE_ERROR
import pandas as pd
from pandas.tests.io.parser import skiprows
from io import StringIO
from builtins import int
import json
# Create your views here.

# class HomePageView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'index.html', context=None)
def homePageView(request):
    return render(request, 'index.html')

# class CrawlingView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'crawling.html', context=None)

def crawlingView(request):
    dataset = []
    data = None
    if request.method=='POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            dataset.append({'judul_berita':row['Judul'], 'konten_berita':row['Konten']})
        data = json.dumps(dataset)                          
    return render(request, 'crawling.html', {'data':data, 'form_input_berita':FormInputBerita, 'form_crawling_berita':PostForm})
    
def hasil(request):
    keyword1 = request.GET.get('keyword', '')
    jumlah1 = request.GET.get('jumlah', 5)
    jumlah1 = int(jumlah1)
    list_news = scrap_detik(keyword1, jumlah1)
    dump = json.dumps(list_news)
    
    return render(request, 'hasil_keyword.html', {'list_news':list_news, 'dump': dump})

# def upload_file(request):
#     
#     
#     return render(request, 'crawling.html', {'header':header, 'list_csv':list_csv})

def word_summary(request):
    list_selected_column = []    

def select_column(request):
    return render(request, 'select_column.html')

def input_berita(request):
    if request.method=='POST':
        form = FormInputBerita(request.POST)
        if form.is_valid():
            judul1 = request.POST['judul_berita']
            konten1 = request.POST['konten_berita']
            query = Tabel_Berita(judul_berita=judul1, konten_berita=konten1)
            query.save()
            return redirect('/crawling')
    else:
        form = FormInputBerita()
    return render(request, 'crawling.html')

def save_crawling(request):
    if request.method=='POST':
        list_berita = request.POST.get('crawling-data')
        list = json.loads(list_berita)
        for row in list:
            judul = row['judul_berita']
            konten = row['konten_berita']
            query = Tabel_Berita(judul_berita=judul, konten_berita=konten)
            query.save()
        return redirect('/crawling')