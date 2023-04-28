from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


#########  DO APP ##################
from .views import download_nota_fiscal
from .views import abrir_nota_fiscal

############################


urlpatterns = [   
    path('accounts/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('homelogout/', views.logout_view, name='homelogout'),
    path('new_user', views.new_user, name='new_user'),

    #path('feedback', views.feedback, name='feedback'),


    path('notaseasy', views.notaseasy, name='notaseasy'),
    path('', views.notaseasy, name='notaseasy'),

    path('notas_fiscais/<int:nota_id>/abrir/', abrir_nota_fiscal, name='abrir_nota_fiscal'),
    path('notas_fiscais/<int:nota_id>/download/', download_nota_fiscal, name='download_nota_fiscal'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
