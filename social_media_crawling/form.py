from django import forms
from django.forms.widgets import DateInput


CHOICES =[('0','API'),('1','SCRAPE')]
lang = [('id','indonesia'),('en','english'),('ja','Japanese'),('ar','arabic'),('es','Spanyol'),('am','amharic')]
class browse_id(forms.Form):
    content = forms.CharField(max_length=500)
    
class advOpt(forms.Form):
    methods = forms.ChoiceField(label= '',choices=CHOICES, widget=forms.RadioSelect(attrs={'onchange': 'formb()'}))

class option(forms.Form):  
    language = forms.CharField(label='bahasa', max_length=2, widget=forms.TextInput(attrs={'placeholder': 'id'}))  

class ScrapeOpt(forms.Form):
    tapdown = forms.IntegerField(min_value=10, widget=forms.TextInput(attrs={'placeholder':20}))

##Fix form
CHOICE = [('0','NO'),('1','YES')]
class upFile(forms.Form):
    file = forms.FileField()

class fixbrowse(forms.Form):
    content = forms.CharField(max_length=500)
    language = forms.ChoiceField(choices=lang,widget=forms.Select(attrs={"class": "selectpicker"}))

class fixscrape(forms.Form):
    tapdown = forms.IntegerField(min_value=10, widget=forms.TextInput(attrs={}))
    date = forms.ChoiceField(label= '',choices=CHOICE, widget=forms.RadioSelect(attrs={'onchange': 'forma("datepick")'}))
    