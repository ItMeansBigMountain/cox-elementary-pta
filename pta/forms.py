
from django import forms
from .models import VolunteerInterest

class VolunteerInterestForm(forms.ModelForm):
    class Meta:
        model = VolunteerInterest
        fields = ['name','email','phone','student_grade','opportunity','message']
        widgets = {'message': forms.Textarea(attrs={'rows':4})}
