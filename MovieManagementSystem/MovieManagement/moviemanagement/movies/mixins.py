from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    """Only allow admin role."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == 'admin'

    def handle_no_permission(self):
        return redirect('movies:home')  # redirect to homepage for non-admin

class UserOnlyReviewMixin(UserPassesTestMixin):
    """Allow only logged-in regular users to add reviews."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_role == 'user'

    def handle_no_permission(self):
        return redirect('movies:signin')
