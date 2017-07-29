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
from crawling.tests import list_news
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from .tables import Berita_Tabel
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
    situs1 = request.GET.get('situs', '')
    jumlah1 = int(jumlah1)
    if situs1=='det':
        list_news = scrap_detik(keyword1, jumlah1)
    elif situs1 == 'kom':
        list_news = crawl_kompas(keyword1, jumlah1)
    elif situs1 == 'lip':
        list_news = crawl_liputan6(keyword1, jumlah1)
    dump = json.dumps(list_news)
     
    return render(request, 'hasil_keyword.html', {'list_news':list_news, 'dump': dump})

# def upload_file(request):
#     
#     
#     return render(request, 'crawling.html', {'header':header, 'list_csv':list_csv})

def word_summary(request):
    list_berita_database = []
    for berita in Tabel_Berita.objects.raw('SELECT * FROM crawling_Tabel_Berita'):
        list_berita_database.append({'judul_berita':berita.judul_berita, 'konten_berita':berita.konten_berita})
    return render(request, 'wordcloud_summary.html', {'list_berita_data':list_berita_database})   

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
        list1 = json.loads(list_berita)
        for row in list1:
            judul = row['judul_berita']
            konten = row['konten_berita']
            query = Tabel_Berita(judul_berita=judul, konten_berita=konten)
            query.save()
        return redirect('/crawling')

def pilih_analisis(request):
    if request.method=='POST':
        list1 = request.POST.get('list-data')
        list2 = json.loads(list1)
        
        print(list2)
    return render(request, 'crawling_mindmap.html', {'list_news':list2})

def data_management_view(request):
    table = Berita_Tabel(Tabel_Berita.objects.all())
    RequestConfig(request, paginate={'per_page':10}).configure(table)
    export_format = request.GET.get('_export', None)
    pks = request.GET.getlist('amend')
    if 'delete' in request.GET:
        sel = Tabel_Berita.objects.filter(pk__in = pks)
        sel.delete()
    selected = Berita_Tabel(Tabel_Berita.objects.filter(pk__in = pks))
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, selected, exclude_columns=('amend'))
        return exporter.response('table.{}'.format(export_format))
    
    
    return render(request, 'data_management.html', {'table':table})

