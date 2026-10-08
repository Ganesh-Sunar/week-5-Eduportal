from django.contrib.auth.models import User
from django.db import models


class StudentRecord(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_records",
        limit_choices_to={"profile__role": "student"},
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="records_added",
    )
    title = models.CharField(max_length=120)
    course = models.CharField(max_length=120)
    attendance = models.PositiveIntegerField(default=0)
    grade = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_add_student_record", "Can add student record"),
            ("can_delete_student_record", "Can delete student record"),
        ]

    def __str__(self):
        return f"{self.title} — {self.student.username}"
