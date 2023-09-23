# decorators.py

def superuser_required(function):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            # You can customize the behavior when the user is not a superuser
            return HttpResponseForbidden("You do not have permission to access this page.")

    return _wrapped_view
