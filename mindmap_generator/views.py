from django.shortcuts import render
from django.http import HttpResponse
from crawling.models import *
from crawling.forms import *
import json
# Create your views here.

from utils.preprocess import initialize_berita
from utils.process import  f2_weight, f4_weight, f5_weight, predict, transform_output

def process_mindmap(request):
    if request.method == 'POST':
        form = FormInputBerita(request.POST)
        if form.is_valid():
            berita = Tabel_Berita.objects.create(judul_berita=form.cleaned_data['judul_berita'], konten_berita=form.cleaned_data['konten_berita'])
            process_berita = initialize_berita(berita.judul_berita, berita.konten_berita)
            f2 = f2_weight(process_berita['token_isi'])
            f4 = f4_weight(process_berita['token_judul'])
            f5 = f5_weight(process_berita['token_isi'], process_berita['token_judul'])
            
            for i, (k, t, f2_, f4_, f5_) in enumerate(zip(process_berita['list_isi'], process_berita['token_isi'], f2, f4, f5)):
                Kalimat.objects.create(
                    kalimat = k,
                    clean = ' '.join(t),
                    f2 = f2_,
                    f4 = f4_,
                    f5 = f5_,
                    index_kalimat = i+1,
                    berita = berita
                    )
            
            prediction = predict(process_berita, f2, f4, f5)
            transformed_output = transform_output(berita.judul_berita, prediction)
            
            return render(request, 'mindmap.html', {'prediction': json.dumps(transformed_output)})
    else:
        return HttpResponse(4)
    
    