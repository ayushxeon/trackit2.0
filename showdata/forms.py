from django import forms

class NameForm(forms.Form):
    location = forms.CharField(label='location', max_length=128)
    vehicle=forms.CharField(label='vehicle',max_length=128)
    weather=forms.CharField(label='weather',max_length=128)