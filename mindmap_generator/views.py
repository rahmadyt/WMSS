from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from crawling.models import Tabel_Berita, Kalimat
from crawling.forms import *
import json

from utils.mindmap.preprocess import initialize_berita
from utils.mindmap.process import *

def process_mindmap(request):
    if request.method == 'POST':
        if request.POST.get('list_berita', 0) == 0:
            output = [create_label_mindmap(request.POST.get('judul_berita'), request.POST.get('konten_berita'))]
        
        else:
            return JsonResponse('kjhkjhk')
        
        return render(request, 'mindmap.html', {'prediction': json.dumps(output), 'range': range(len(output))})
    else:
        return HttpResponse(4)
    
def create_model(request):
    all = Kalimat.objects.filter(accepted=True).filter(f2__gt=0.0).filter(f4__gt=0.0).filter(f5__gt=0.0)
    k = [kalimat.clean for kalimat in all]
    update_model(all)
    return JsonResponse(k, safe=False)
    
def create_label_mindmap(judul, konten):
    berita = Tabel_Berita.objects.create(judul_berita=judul, konten_berita=konten)
    process_berita = initialize_berita(berita.judul_berita, berita.konten_berita)
    f2 = f2_weight(process_berita['token_isi'])
    f4 = f4_weight(process_berita['token_judul'])
    f5 = f5_weight(process_berita['token_isi'], process_berita['token_judul'])
    
    prediction = predict(process_berita, f2, f4, f5)
    for i, (p, k, t, f2_, f4_, f5_) in enumerate(zip(prediction, process_berita['list_isi'], process_berita['token_isi'], f2, f4, f5)):
        tipe = list()
        if(p['kode'][0]):
            tipe.append('apa')
        if(p['kode'][1]):
            tipe.append('dimana')
        if(p['kode'][2]):
            tipe.append('bagaimana')
        if(p['kode'][3]):
            tipe.append('kapan')
        if(p['kode'][4]):
            tipe.append('siapa')
        if(p['kode'][5]):
            tipe.append('mengapa')
            
        tipe = ', '.join(tipe)
        Kalimat.objects.create(
            kalimat = k,
            clean = ' '.join(t),
            f2 = f2_,
            f4 = f4_,
            f5 = f5_,
            index_kalimat = i+1,
            tipe = tipe,
            berita = berita
            )
    
    transformed_output = transform_output(berita.judul_berita, prediction, f5)
    
    return transformed_output
    
def verify():
    pass

def process_mindmap1(request):
    if request.method == 'POST':
        judul = request.POST.get('judul_berita', None)
        konten = request.POST.get('konten_berita', None)
        if request.POST.get('list_berita', 0) == 0:
            output = [create_label_mindmap(judul, konten)]
        
        else:
            return JsonResponse('kjhkjhk')
        
        return render(request, 'mindmap.html', {'prediction': json.dumps(output), 'range': range(len(output))})
    else:
        return HttpResponse(4)
    