# Week 5 — Role-Based Student Portal

A Django + Bootstrap internship assignment project covering:

- User registration, login, logout
- Password change and basic password reset
- Unique email + username validation
- Role system: Student, Teacher, Admin
- Login protection with `login_required`
- `LoginRequiredMixin`
- `PermissionRequiredMixin`
- Custom permissions
- Custom role decorators
- UserProfile with OneToOne User relation
- Profile picture, bio, phone and address
- Separate Student / Teacher / Admin dashboards
- StudentRecord CRUD using Class-Based Views
- `get_queryset()`, `get_context_data()`, `form_valid()`, `dispatch()`
- User-specific data filtering
- Django messages
- Bootstrap responsive UI
- Django admin support

## 1. Setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin:

```bash
python manage.py createsuperuser
```

Run:

```bash
python manage.py runserver
```

Open:

`http://127.0.0.1:8000/`

## 2. Roles

Registration allows Student or Teacher.

Admin is intentionally not available in public registration. Create the admin with:

```bash
python manage.py createsuperuser
```

The first superuser automatically gets an Admin profile through the signal.

You can also change a user's role from Django admin.

## 3. Demo flow

1. Register a Student account.
2. Register a Teacher account.
3. Log in as Teacher.
4. Add a Student Record.
5. Log in as Student and see only that student's records.
6. Log in as Admin and inspect the admin dashboard.
7. Try protected URLs while logged out to verify authorization.

## 4. Password reset

The reset flow is configured with Django's console email backend for development. When a reset email is sent, the reset link is printed in the terminal.

## 5. Main URLs

- `/` — landing page
- `/accounts/register/`
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/password/change/`
- `/accounts/password/reset/`
- `/accounts/profile/`
- `/dashboard/`
- `/portal/students/`
- `/portal/students/add/`
- `/portal/students/<id>/`
- `/portal/students/<id>/edit/`
- `/portal/students/<id>/delete/`
- `/admin/`

## 6. Week 5 requirement mapping

| Requirement | Implementation |
|---|---|
| Registration | `accounts/forms.py`, `RegisterView` |
| Login/logout | Django built-in auth views |
| Password change/reset | Built-in auth views |
| Unique email | `RegisterForm.clean_email()` |
| Username restriction | `RegisterForm.clean_username()` |
| Route protection | `login_required`, `LoginRequiredMixin` |
| Roles | `UserProfile.role` + Groups |
| Dashboards | `portal/views.py` |
| `has_perm()` | `portal/views.py` |
| `PermissionRequiredMixin` | `StudentRecordDeleteView` |
| Custom permission | `can_add_student_record`, `can_delete_student_record` |
| Profile | `UserProfile` OneToOne User |
| List/Detail/Create/Update/Delete | CBVs in `portal/views.py` |
| `get_queryset()` | student/teacher filtering |
| `get_context_data()` | dashboard context |
| `form_valid()` | record ownership / creator |
| `dispatch()` | role protection |
| User-specific data | filtered querysets |
| Messages | auth + CRUD views |
| Custom role decorators | `accounts/decorators.py` |

Optional bonus tasks such as email verification, remember-me, account deactivation, and last-login display are not required for the core submission.
