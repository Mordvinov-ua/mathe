from django.contrib.auth.views import LoginView
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = 'index.html'

    def get_success_url(self):
        return reverse('home')