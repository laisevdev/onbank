from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class SlidingTokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(id=user_id).first()
            request.user = user if user else AnonymousUser()
        else:
            request.user = AnonymousUser()
