from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('api/toggle-like/', views.toggle_like, name='toggle_like'),
    path('api/toggle-follow/', views.toggle_follow, name='toggle_follow'),
    path('api/add-comment/', views.add_comment, name='add_comment'),
]