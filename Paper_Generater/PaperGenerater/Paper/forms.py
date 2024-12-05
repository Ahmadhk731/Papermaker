# forms.py
from django import forms
from .models import Grade, Subject, Chapter

class GradeSelectionForm(forms.Form):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=True, label="Select Grade")

class SubjectSelectionForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=True, label="Select Subject")

    def __init__(self, *args, **kwargs):
        grade = kwargs.pop('grade', None)
        super().__init__(*args, **kwargs)
        if grade:
            # Filter subjects based on selected grade
            self.fields['subject'].queryset = Subject.objects.filter(grade=grade)

class ChapterSelectionForm(forms.Form):
    chapter = forms.ModelChoiceField(queryset=Chapter.objects.none(), required=True, label="Select Chapter")

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        if subject:
            # Filter subjects based on selected grade
            self.fields['chapter'].queryset = Chapter.objects.filter(subject=subject)
