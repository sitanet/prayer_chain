from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('select-time/', views.select_time_view, name='select_time'),
    path('success/', views.success_view, name='success'),
    path('report/', views.report_view, name='report'),
    path('new-registration/', views.new_registration_view, name='new_registration'),
]