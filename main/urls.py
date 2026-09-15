# URL routes configuration for main pages (Home, About, Contact)
from django.urls import path
from . import views
urlpatterns = [
    path("", views.home_page, name="home"),
    path("about-us/", views.about_page, name="about-us"),
    path("contact-us/", views.contact_us, name="contact_us")
]