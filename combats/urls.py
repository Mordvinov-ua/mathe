from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('characters.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]