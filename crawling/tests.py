from django.test import TestCase

from bs4 import BeautifulSoup
import requests
import urllib.request

# arai = [('nasi', 'buah', 'sayur'), ('susu', 'soya', 'kedelai')]
# print(arai[1][0])
# csv_file = 'C:/Users/Asus-PC/Desktop/detik_testing.csv'
# df = pd.read_csv(csv_file)
# data = df.as_matrix(columns=None)
# list =[]
# for row in data:
#     list.append(row)
# print(list[0][1])

#     # membuat koneksi ke url 
#     page= urllib.request.urlopen(url1)
#     html = page.read()
#  
#     # membaca html
#     soup = BeautifulSoup(html, "html.parser")
# #======================================================================================================================
#     # fungsi bs4
#     test = soup.findAll(string=re.compile(keyword1, re.IGNORECASE))
#     list_search = []
#     for tag in test:    
# #         query = Hasil_Pencarian_Keyword(word_result=tag)
# #         query.save()
#         list_search.append(tag)
# list_berita=[]
def scrap_detik_page(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    judul = soup.find('a',{'data-title': True})
    judul_berita = judul['data-title']
    konten = soup.find('div',attrs={'id':'detikdetailtext'})
    konten_berita = konten.text.strip().splitlines()[0]

    return {'judul_berita': judul_berita, 'konten_berita': konten_berita}
#     list_berita.append({'judul_berita':judul_berita, 'konten_berita':konten_berita})

def scrap_detik(keyword, jumlah):
    url = 'https://www.detik.com/search/searchall?query='+keyword+'&source=dcnav&siteid=2'
    return get_link_detik(url, jumlah, list())

def get_link_detik(url, jumlah, data):
    page = requests.get(url)
    content = page.content
    soup_page = BeautifulSoup(content, 'html.parser')
    for article in soup_page.select('div.list-berita > article'):
        if article.has_attr('class'):
            continue
        berita = scrap_detik_page(article.find('a')['href'])
        data.append(berita) #ganti dengan method scarp halaman berita detik
        if len(data)==jumlah:
            break
    if len(data)<jumlah:
        next_page = soup_page.find('div', class_='paging')
        next_page= next_page.find('a', class_='last')['href']
        return get_link_detik(next_page, jumlah, data)
    else:
        return data
