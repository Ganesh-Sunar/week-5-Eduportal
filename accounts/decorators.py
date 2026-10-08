from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def role_required(*roles):
    """Custom role decorator used to protect function-based views."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            role = getattr(getattr(request.user, "profile", None), "role", None)
            if request.user.is_superuser:
                role = "admin"
            if role not in roles:
                messages.error(request, "You do not have permission to access this page.")
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
