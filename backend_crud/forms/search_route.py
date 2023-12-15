from django import forms

class SearchRouteForm(forms.Form):
    to_location = forms.CharField()
    from_location =forms.CharField()
    departure_time = forms.DateTimeField()
    