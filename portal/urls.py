from django.urls import path
from .views import (
    AdminDashboardView,
    StudentDashboardView,
    StudentRecordCreateView,
    StudentRecordDeleteView,
    StudentRecordDetailView,
    StudentRecordListView,
    StudentRecordUpdateView,
    TeacherDashboardView,
)

urlpatterns = [
    path("student-dashboard/", StudentDashboardView.as_view(), name="student_dashboard"),
    path("teacher-dashboard/", TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),

    path("students/", StudentRecordListView.as_view(), name="record_list"),
    path("students/add/", StudentRecordCreateView.as_view(), name="record_create"),
    path("students/<int:pk>/", StudentRecordDetailView.as_view(), name="record_detail"),
    path("students/<int:pk>/edit/", StudentRecordUpdateView.as_view(), name="record_update"),
    path("students/<int:pk>/delete/", StudentRecordDeleteView.as_view(), name="record_delete"),
]
