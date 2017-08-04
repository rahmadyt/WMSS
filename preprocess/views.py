from django.shortcuts import render
from .ED_rule import correction_3, bigram_corr5
from .tests import getall

# Create your views here.
def index(request):
    tp = ['Edit Distance + Rule','Bigram']
    input = ''
    hasil = ''
    textb = []
    if request.method=="POST":
        if 'inputA' in request.POST:
            PR = request.POST.get("PR")
            input = request.POST.get('inputtext')
            hasil = correction_3(input)
        if 'inputB' in request.POST:
#             b = getall()
            textb = bigram_corr5()
#             textb = bigram_corr5(b['twits'])
    return render(request, 'index_preprocess.html',{'input':input, 'hasil':hasil,'data':tp,'text1':textb})

def index2(request):
    tp = ['Edit Distance + Rule','Bigram']
    input = ''
    hasil = ''
    textb = []
    if request.method=="POST":
            PR = request.POST.get("PR")
            input = request.POST.get('konten_berita')
            hasil = correction_3(input)
    return render(request, 'index_preprocess.html',{'input':input, 'hasil':hasil,'data':tp,'text1':textb})

