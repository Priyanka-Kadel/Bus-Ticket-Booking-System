from django import forms
from backend_crud.models import  Schedule
import re
from datetime import datetime


class PassengerForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)
    email=forms.EmailField( required=True)
    contact=forms.CharField(max_length=10, required=True)
    from_location=forms.CharField(required=True)
    to_location=forms.CharField(required=True)
    reserved_seats=forms.CharField(required=True)
    scheduled_id=forms.IntegerField()

    
    def clean_name(self):
        return self.cleaned_data.get('name').strip()
    
    def clean_email(self):
        # passenger_details =PassengerDetails.objects.filter(email=self.cleaned_data.get ('email').strip())
        # if passenger_details.exists():
        #     raise forms.ValidationError("Passenger Exists")
        return self.cleaned_data.get('email').strip()
    
    def clean_contact(self):
        pattern = r'\d'  # \d matches any digit (0-9)
        if not bool(re.search(pattern, self.cleaned_data.get('contact').strip())):
            raise forms.ValidationError("Invalid Contact Number")

        
        return self.cleaned_data.get("contact").strip()

        
        
    def clean(self):
        

        # route = Route.objects.filter(from_location= self.cleaned_data.get('from_location'), to_location= self.cleaned_data.get('to_location')).first()
        schedule= Schedule.objects.filter(route__from_location= self.cleaned_data.get('from_location'), route__to_location= self.cleaned_data.get('to_location'), departure_time__date=datetime.now()).first()
        print(schedule)
        self.cleaned_data.pop('from_location')
        self.cleaned_data.pop('to_location')
        self.cleaned_data.update({'schedule':schedule})
        return self.cleaned_data
    