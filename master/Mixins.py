
from Mufo import settings 
from django.http import HttpResponse,JsonResponse

from master.models import Common

def authenticate_token(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        models = [Common,]
        user = None

        for model in models:
            try:
                user = model.objects.get(token=token)
                break
            except model.DoesNotExist:
                continue

        if user is None:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper

