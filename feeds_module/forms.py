from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': "What's new?",
                'class': 'h-28 textarea textarea-bordered w-full rounded-lg',
            }
        ),
        label="",
    )

    class Meta:
        model = Post
        fields = ('text',)