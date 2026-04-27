from django import forms
from models.models import Category

SORT_CHOICES = [
    ("name", "Name"),
    ("age", "Age"),
    ("category", "Category"),
]

class PeopleForm(forms.Form):
    DEFAULTS = {
        "sort": "name",
        "age_from": 0, 
        "age_to": 100,
        "page_num": 1, 
        "category": Category.objects.all(),
    }


    sort = forms.ChoiceField(label="Sort by", choices=SORT_CHOICES, required=False)
    age_from = forms.IntegerField(label="From", min_value=0, max_value=100, required=False)
    age_to = forms.IntegerField(label="To", min_value=0, max_value=100, required=False)
    size = forms.IntegerField(label="Size", min_value=1, max_value=10000, required=False)
    page_num = forms.IntegerField(label="Page", min_value=1, required=False)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean(self):
        cleaned = super().clean()
        for key, default in self.DEFAULTS.items():
            if cleaned.get(key) is None:
                cleaned[key] = default
        return cleaned
