from django import forms

from MyApp.models import *

class CartForm(forms.ModelForm):
    class Meta():
        model=Cart
        fields=['count']