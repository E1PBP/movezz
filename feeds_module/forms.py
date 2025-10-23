from django import forms
from .models import Post, PostImage
from common.models import Sport

class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': "Type here",
                'class': 'textarea textarea-bordered w-full rounded-lg h-32',
            }
        ),
        label="",
        required=False,
    )
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'select select-bordered w-full',
            }
        ),
        required=False,
        empty_label="Select a sport"
    )
    location_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type here...',
                'class': 'input input-bordered w-full',
            }
        ),
        required=False
    )

    class Meta:
        model = Post
        fields = ('text', 'sport', 'location_name')

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']