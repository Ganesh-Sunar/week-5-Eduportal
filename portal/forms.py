from django import forms
from django.contrib.auth.models import User
from .models import StudentRecord


class StudentRecordForm(forms.ModelForm):
    class Meta:
        model = StudentRecord
        fields = ("student", "title", "course", "attendance", "grade", "notes")
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"placeholder": "e.g. Web Development"}),
            "course": forms.TextInput(attrs={"placeholder": "e.g. Django"}),
            "attendance": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "grade": forms.TextInput(attrs={"placeholder": "A, B+, etc."}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Teacher notes..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = User.objects.filter(
            is_active=True, profile__role="student"
        ).select_related("profile")
