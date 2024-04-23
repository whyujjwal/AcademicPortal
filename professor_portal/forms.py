from django import forms

class StudentSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Students', max_length=100)