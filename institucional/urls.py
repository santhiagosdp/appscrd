from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [   
    path('accounts/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('homelogout/', views.logout_view, name='homelogout'),
    path('new_user', views.new_user, name='new_user'),

    #path('feedback', views.feedback, name='feedback'),


    path('home', views.home, name='home'),
    path('', views.home, name='home'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
