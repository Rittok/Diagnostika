from django import forms
from .models import School, ClassLevel

class ReportFilterForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=False)
    class_level = forms.ModelMultipleChoiceField(queryset=ClassLevel.objects.all(), required=False)