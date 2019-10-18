from django import forms
from material import Row, Layout, Span10, Span2

RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


class ReviewForm(forms.Form):
    text = forms.CharField(max_length=2000)
    rating = forms.ChoiceField(choices=RATING_CHOICES)

    layout = Layout(Row(Span10('text'), Span2('rating')))

    # def __init__(self, *args, **kwargs):
    #     super(ReviewForm, self).__init__(*args, **kwargs)
    #     self.fields['rating'].widget.choices = RATING_CHOICES
