
from django import forms
from .models import VolunteerInterest

class VolunteerInterestForm(forms.ModelForm):
    class Meta:
        model = VolunteerInterest
        fields = ['name','email','phone','student_grade','opportunity','message']
        labels = {'opportunity': 'Opportunity'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'student_grade': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'message': forms.Textarea(attrs={'rows':4, 'placeholder': 'Tell us when you can help or what you are interested in.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opportunity_field = self.fields['opportunity']
        opportunity_field.empty_label = None
        if opportunity_field.queryset.exists():
            opportunity_field.initial = opportunity_field.queryset.first()
        else:
            opportunity_field.required = False
            opportunity_field.widget = forms.HiddenInput()
