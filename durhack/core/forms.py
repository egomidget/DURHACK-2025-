from django import forms
from .models import Question

class DynamicQuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(
            label = "Your name",
            widget=forms.Textarea(
                    attrs={
                        "rows": 1,
                        "class": "form-control",
                        "placeholder": "Type your answer..."
                    }
                ),
            required=True
        )

        for question in questions:
            
            field_name = f"question_{question.id}"
            self.fields[field_name] = forms.IntegerField(
                label=question.text,
                widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'min': '0', 'max': '10', 'class':'form-range'}), 
                required=False)
            
        
    
