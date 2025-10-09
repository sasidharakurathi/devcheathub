# core/forms.py
from django import forms

class JSONContributionForm(forms.Form):
    json_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80,'autocomplete': 'off'}),
        label="Paste your formatted JSON here",
        help_text="Ensure your JSON follows the required structure."
    )