from django import forms

class MyFileForm(forms.Form):
    file = forms.FileField()