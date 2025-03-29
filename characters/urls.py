from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('fight/', views.fight, name='fight'),
    path('update_character_after_battle/<int:character_id>/', views.update_character_after_battle, name='update_character_after_battle'),
    path('update_character_health/<int:character_id>/', views.update_character_health, name='update_character_health'),
    path('distribute_skill_points/<int:character_id>/', views.distribute_skill_points, name='distribute_skill_points'),
]


