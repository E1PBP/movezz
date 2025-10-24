from django import forms
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
    location_lat = forms.FloatField(required=False)
    location_lng = forms.FloatField(required=False)
    fee = forms.IntegerField(required=True, min_value=0)
    image = forms.ImageField(required=False)
    rsvp_url = forms.URLField(required=True)


