from django import forms

class ApartmentForm(forms):
  name = forms.CharField(label="Search Name")