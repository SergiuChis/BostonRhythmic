from django import forms

class XlsDiffForm(forms.Form):
    old_file = forms.FileField()
    new_file = forms.FileField()
