from django import forms
from django.core.exceptions import ValidationError


class CreatePostForm(forms.Form):
    caption = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Type here…",
                "class": "w-full rounded-lg border px-3 py-2",
            }
        ),
        label="Caption",
    )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"accept": "image/*", "class": "block"}
        ),
        label="Image (Upload)",
    )

    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                "placeholder": "or paste image URL",
                "class": "rounded-lg border px-3 py-2 w-full",
            }
        ),
        label="Image URL",
    )

    tournament = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(
            attrs={"placeholder": "Type here…", "class": "rounded-lg border px-3 py-2 w-full"}
        ),
        label="Tournament",
    )

    exercise = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(
            attrs={"placeholder": "Type here…", "class": "rounded-lg border px-3 py-2 w-full"}
        ),
        label="Exercise",
    )

    time_h = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(
            attrs={"placeholder": "00", "class": "w-16 rounded-lg border px-2 py-2 text-center"}
        ),
        label="Hours",
    )

    time_m = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59,
        widget=forms.NumberInput(
            attrs={"placeholder": "00", "class": "w-16 rounded-lg border px-2 py-2 text-center"}
        ),
        label="Minutes",
    )

    def clean(self):
        cleaned = super().clean()
        image = cleaned.get("image")
        image_url = cleaned.get("image_url")

        if not image and not image_url:
            raise ValidationError("Harap unggah gambar atau isi Image URL.")

        return cleaned

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
        if getattr(image, "size", 0) > 10 * 1024 * 1024:
            raise ValidationError("Ukuran gambar maksimal 10MB.")
        return image

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
