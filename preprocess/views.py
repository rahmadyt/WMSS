from django.shortcuts import render
from .skripsi2 import correction_3, bigram_corr5
from .tests import getall

# Create your views here.
def index(request):
    tp = ['Edit Distance','Bigram']
    texta = ''
    textb = []
    if request.method=="POST":
        if 'inputA' in request.POST:
            PR = request.POST.get("PR")
            texta = request.POST.get('inputtext')
            texta = correction_3(texta)
        if 'inputB' in request.POST:
            b = getall()
            textb = bigram_corr5(b['twits'])
    return render(request, 'index_preprocess.html',{'text':texta,'data':tp,'text1':textb})