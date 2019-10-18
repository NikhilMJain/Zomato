from django import forms


class SearchQueryForm(forms.Form):
    search_dish = forms.CharField(max_length=300)
