from django import forms

class SearchRouteForm(forms.Form):
    to_location = forms.CharField(required=False)
    from_location =forms.CharField(required=False)
    departure_time = forms.DateTimeField()
    