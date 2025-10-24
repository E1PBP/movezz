from django import forms
from django.core.exceptions import ValidationError
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "description",
            "start_time",
            "end_time",
            "location_name",
            "location_lat",
            "location_lng",
            "fee",
            "image",
            "rsvp_url",
        ]

    start_time = forms.DateTimeField(
        required=True, 
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    end_time = forms.DateTimeField(
        required=True, 
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    location_name = forms.CharField(required=True)
    location_lat = forms.DecimalField(
        required=False, 
        max_digits=9, 
        decimal_places=6,
        min_value=-90,
        max_value=90
    )
    location_lng = forms.DecimalField(
        required=False, 
        max_digits=9, 
        decimal_places=6,
        min_value=-180,
        max_value=180
    )
    fee = forms.IntegerField(required=True, min_value=0)
    image = forms.ImageField(required=False)
    rsvp_url = forms.URLField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        location_lat = cleaned_data.get('location_lat')
        location_lng = cleaned_data.get('location_lng')

        # Beri pesan error ketika hanya salah satu koordinat yang diisi
        if (location_lat is not None and location_lng is None) or (location_lat is None and location_lng is not None):
            raise ValidationError("Both latitude and longitude must be provided together, or leave both empty.")

        return cleaned_data


