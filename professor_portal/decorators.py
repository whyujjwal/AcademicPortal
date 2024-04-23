from django.contrib.auth.decorators import user_passes_test
from base.models import Professor

def professor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            professor = request.user.professor
            return view_func(request, *args, **kwargs)
        except Professor.DoesNotExist:
            return redirect('unauthorized')
    return _wrapped_view
