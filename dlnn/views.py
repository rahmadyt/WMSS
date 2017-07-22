from django.shortcuts import render
from dlnn.listFunction import gabungdata

# Create your views here.
def index(request):
    FeatX = ['1 TF','2 TF-IDF','3 BOW','4 nGRAM']
    predict = ''
    IA = ''
    if request.method=="POST":
        if 'input' in request.POST:
            
            FE = request.POST.get("FE")
            IA = request.POST.get("inputArea")
            predict = gabungdata(IA,int(FE))
            
    return render(request, "index_dlnn.html",{'data':FeatX,'sent':predict, 'IA':IA})