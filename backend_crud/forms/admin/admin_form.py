# forms.py
from django import forms
from django.contrib import admin
from backend_crud.models import BusSeatStatus
from django.db.models import Count, Case, Value, When
from django.db import models

class BusSeatStatusAdminForm(forms.ModelForm):
    class Meta:
        model = BusSeatStatus
        fields = '__all__'

    def clean(self):
        # Add your custom validation logic here
        data = self.cleaned_data['schedule']
        seat_side_counts = BusSeatStatus.objects.filter(schedule=data)
        

        seat_a = seat_side_counts.filter(seat_side = 'A')
        seat_b = seat_side_counts.filter(seat_side = 'B')


        if self.cleaned_data.get('seat_side')== 'A' and seat_a.count()>=20:
            raise forms.ValidationError("Total seat in side A cannot be greater than 10")
        if self.cleaned_data.get('seat_side')== 'B' and seat_b.count()>=20:
            raise forms.ValidationError("Total seat in side B cannot be greater than 10")

        return super().clean()
