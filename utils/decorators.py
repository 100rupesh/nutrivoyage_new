# utils/decorators.py (or wherever you want to keep it)
from django.shortcuts import render
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user_role = getattr(request.user, 'role', None)
            print("Role",user_role)
            if user_role not in allowed_roles:
                return render(request,'dashboard/access_denied.html')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
