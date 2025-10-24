from django import forms
from django.core.exceptions import ValidationError

class PostUpdateForm(forms.Form):
    caption = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Update caption…",
                "class": "w-full rounded-lg border px-3 py-2",
            }
        ),
        label="Caption",
    )
