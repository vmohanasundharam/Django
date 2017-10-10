from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^worldsearch/search/', views.search, name='search'),
    url(r'^worldsearch/display/', views.search, name='search'),
    url(r'^worldsearch/country_details/', views.country_details, name='country_details'),
    url(r'^worldsearch/register/', views.register, name='register'),
    url(r'^worldsearch/login/', views.login, name='login'),
    url(r'^worldsearch/otp/', views.otp, name='otp'),
    url(r'^worldsearch/', views.index, name='index'),
    url(r'^worldsearch/logout', views.logout, name='logout'),


]
