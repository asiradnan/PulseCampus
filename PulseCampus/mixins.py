from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class PrincipalRequiredMixin(UserPassesTestMixin):
    raise_exception = PermissionDenied  
    def test_func(self):
        return hasattr(self.request.user, 'principal')
    
class TeacherOrPrincipalRequiredMixin(UserPassesTestMixin):
    raise_exception = PermissionDenied
    def test_func(self):
        return hasattr(self.request.user, 'principal') or hasattr(self.request.user, 'teacher')
    
def is_principal(user):
    return hasattr(user, 'principal')