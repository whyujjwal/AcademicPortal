from django import forms
from base.models import Course, Eval

class StudentSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Students', max_length=100)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'department', 'course_incharge', 'credit']

class EvalForm(forms.ModelForm):
    class Meta:
        model = Eval
        fields = ['name', 'max_marks']