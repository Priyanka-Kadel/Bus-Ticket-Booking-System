from django import forms
from backend_crud.models import PassengerDetails ,Route

class PassengerForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)
    email=forms.EmailField( required=True)
    contact=forms.CharField(max_length=10, required=True)
    from_location=forms.CharField(required=True)
    to_location=forms.CharField(required=True)
    
    def clean_name(self):
        return self.cleaned_data.get('name').strip()
    
    def clean_email(self):
        # passenger_details =PassengerDetails.objects.filter(email=self.cleaned_data.get ('email').strip())
        # if passenger_details.exists():
        #     raise forms.ValidationError("Passenger Exists")
        return self.cleaned_data.get('email').strip()
    
    def clean_contact(self):
        # if PassengerDetails.objects.filter(contact=self.cleaned_data.get("contact").strip()).exists():
        #     raise forms.ValidationError("This number already exists")
        return self.cleaned_data.get("contact").strip()
        
    def clean(self):
        route = Route.objects.filter(from_location= self.cleaned_data.get('from_location'), to_location= self.cleaned_data.get('to_location')).first()
        self.cleaned_data.pop('from_location')
        self.cleaned_data.pop('to_location')
        self.cleaned_data.update({'route':route})
        print(self.cleaned_data)
        return self.cleaned_data
    