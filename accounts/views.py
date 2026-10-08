from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import ProfileForm, RegisterForm
from .models import UserProfile


class HomeView(TemplateView):
    template_name = "home.html"


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Welcome! Your account has been created successfully.")
        return redirect("dashboard")

    def get_success_url(self):
        return "/dashboard/"


class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = "accounts/profile.html"
    success_url = "/accounts/profile/"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)


class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard_redirect.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.profile.role == "admin":
            return redirect("admin_dashboard")
        if request.user.profile.role == "teacher":
            return redirect("teacher_dashboard")
        return redirect("student_dashboard")
