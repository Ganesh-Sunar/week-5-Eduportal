from django.contrib import admin
from .models import StudentRecord

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "course", "grade", "attendance", "added_by", "created_at")
    list_filter = ("course", "grade")
    search_fields = ("title", "course", "student__username", "added_by__username")
