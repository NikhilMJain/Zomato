from django import forms
from material import Layout, Row, Span4


class SearchType:
    RESTAURANT_TYPE = 'Restaurant Type'
    RESTAURANT_CATEGORY = 'Restaurant Category'
    CUISINE = 'Cuisine'

    CHOICES = (
        (RESTAURANT_CATEGORY, RESTAURANT_CATEGORY),
        (RESTAURANT_TYPE, RESTAURANT_TYPE),
        (CUISINE, CUISINE)
    )


class SearchForm(forms.Form):
    search_by = forms.ChoiceField(choices=SearchType.CHOICES)
    search_text = forms.CharField(max_length=200)

    layout = Layout(Row(Span4('search_by')), Row('search_text'))
