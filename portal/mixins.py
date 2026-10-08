from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View


class RoleRequiredMixin(View):
    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        role = "admin" if request.user.is_superuser else request.user.profile.role
        if role not in self.allowed_roles:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("dashboard")

        return super().dispatch(request, *args, **kwargs)
