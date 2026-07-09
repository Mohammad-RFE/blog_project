from django.urls import path
from . import views
urlpatterns = [
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("user/panel/", views.user_panel, name="user panel"),
    path("user/<str:username>", views.user_public_profile, name="user public profile"),
    path('profile/delete-image/', views.delete_profile_image_ajax, name='delete_profile_image'),
]