"""WMSS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from crawling import views
from mindmap_generator import views as views_mindmap

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homePageView, name='homePageView'),
    url(r'^crawling/$', views.crawlingView, name='crawlingView'),
    url(r'^data_management/$', views.data_management_view, name='data_management_view'),
    url(r'^crawling/hasil_keyword/', views.hasil, name='hasil'),
    url(r'^crawling/word_summary/$', views.word_summary, name='word_summary'),
    url(r'^crawling/input_berita/$', views.input_berita, name='input_berita'),
    url(r'^crawling/word_summary/berita/$', views.get_berita, name='get_berita'),
    url(r'^mindmap/process/$', views_mindmap.process_mindmap, name='process_mindmap'),
    url(r'^mindmap/process1/$', views_mindmap.process_mindmap1, name='process_mindmap1'),
    url(r'^mindmap/verify-prediction', views_mindmap.verify, name='verify_prediction'),
    url(r'^mindmap/update-model', views_mindmap.create_model, name='update_model'),
    url(r'^crawling/save_crawling/', views.save_crawling, name='save_crawling'),
    url(r'^crawling/pilih_analisis/', views.pilih_analisis, name='pilih_analisis'),
    url(r'^social_media_crawling/', include('social_media_crawling.urls')),
    url(r'^preprocess/', include('preprocess.urls'))
#     url(r'^dlnn/', include('dlnn.urls'))
]
