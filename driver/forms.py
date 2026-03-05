from django import forms
from .models import Inspection, Issue

class PreInspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['brakes_ok', 'tires_ok', 'fluids_ok', 'lug_nuts_ok', 'shocks_ok', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any abnormalities noticed?'}),
        }

class PostInspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['brakes_ok', 'tires_ok', 'fluids_ok', 'lug_nuts_ok', 'shocks_ok', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any abnormalities noticed?'}),
        }

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['description', 'severity', 'location']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'e.g., Rear left tire has a deep puncture, air pressure dropping rapidly...'
            }),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Logistics Hub 42 - Chicago, IL'}),
        }
