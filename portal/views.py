from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from accounts.decorators import role_required
from .forms import StudentRecordForm
from .mixins import RoleRequiredMixin
from .models import StudentRecord


class StudentDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "portal/student_dashboard.html"
    allowed_roles = ("student",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = StudentRecord.objects.filter(student=self.request.user)
        context["records"] = records
        context["record_count"] = records.count()
        return context


class TeacherDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "portal/teacher_dashboard.html"
    allowed_roles = ("teacher",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_count"] = User.objects.filter(profile__role="student").count()
        context["record_count"] = StudentRecord.objects.filter(added_by=self.request.user).count()
        context["recent_records"] = StudentRecord.objects.filter(
            added_by=self.request.user
        ).select_related("student")[:5]
        return context


class AdminDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "portal/admin_dashboard.html"
    allowed_roles = ("admin",)

    def get_context_data(self, **kwargs):
        from accounts.models import UserProfile
        context = super().get_context_data(**kwargs)
        context["student_count"] = UserProfile.objects.filter(role="student").count()
        context["teacher_count"] = UserProfile.objects.filter(role="teacher").count()
        context["record_count"] = StudentRecord.objects.count()
        return context


class StudentRecordListView(LoginRequiredMixin, ListView):
    model = StudentRecord
    template_name = "portal/record_list.html"
    context_object_name = "records"

    def get_queryset(self):
        """Filter data according to the logged-in user's role."""
        user = self.request.user
        if user.is_superuser or user.profile.role == "admin":
            return StudentRecord.objects.select_related("student", "added_by")
        if user.profile.role == "teacher":
            return StudentRecord.objects.filter(added_by=user).select_related("student")
        return StudentRecord.objects.filter(student=user).select_related("student", "added_by")


class StudentRecordDetailView(LoginRequiredMixin, DetailView):
    model = StudentRecord
    template_name = "portal/record_detail.html"
    context_object_name = "record"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.profile.role == "admin":
            return StudentRecord.objects.all()
        if user.profile.role == "teacher":
            return StudentRecord.objects.filter(added_by=user)
        return StudentRecord.objects.filter(student=user)


class StudentRecordCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = StudentRecord
    form_class = StudentRecordForm
    template_name = "portal/record_form.html"
    allowed_roles = ("teacher",)

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, "Student record created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return "/portal/students/"


class StudentRecordUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = StudentRecord
    form_class = StudentRecordForm
    template_name = "portal/record_form.html"
    allowed_roles = ("teacher", "admin")

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.profile.role == "admin":
            return StudentRecord.objects.all()
        return StudentRecord.objects.filter(added_by=user)

    def form_valid(self, form):
        messages.success(self.request, "Student record updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return "/portal/students/"


class StudentRecordDeleteView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DeleteView):
    model = StudentRecord
    template_name = "portal/record_confirm_delete.html"
    permission_required = "portal.can_delete_student_record"
    raise_exception = False
    allowed_roles = ("admin",)

    def has_permission(self):
        return self.request.user.is_superuser or self.request.user.has_perm(
            self.permission_required
        )

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.profile.role == "admin":
            return StudentRecord.objects.all()
        return StudentRecord.objects.none()

    def form_valid(self, form):
        messages.success(self.request, "Student record deleted successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return "/portal/students/"
