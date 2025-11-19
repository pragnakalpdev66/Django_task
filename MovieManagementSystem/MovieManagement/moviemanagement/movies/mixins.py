from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # type: ignore
from django.shortcuts import redirect # type: ignore
from django.contrib import messages # type: ignore

class AdminRequiredMixin(UserPassesTestMixin):
    """Only allow admin role."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == 'admin'

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('movies:home')  

class UserAccessMixin(LoginRequiredMixin):
    """Allow only logged-in regular users to add reviews."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == 'user'

    def handle_no_permission(self):
        return redirect('movies:signin')
