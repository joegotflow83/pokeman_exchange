from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse

from .forms import UserForm
from .models import UserProfile


class Signup(CreateView):
    """Allow user to sign up"""
    model = User
    form_class = UserForm

    def form_valid(self, form):
        """Validate the form"""
        new_user = form.save(commit=False)
        new_user.user = self.request.user
        new_user.save()
        UserProfile.objects.create(user=new_user, profile_pic=form.cleaned_data['profile_pic'])
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to login page"""
        return reverse('login')
