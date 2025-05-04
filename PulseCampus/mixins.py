from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class PrincipalRequiredMixin(UserPassesTestMixin):
    raise_exception = PermissionDenied  
    def test_func(self):
        return hasattr(self.request.user, 'principal')
    
def is_principal(user):
    return hasattr(user, 'principal')