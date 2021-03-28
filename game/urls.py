from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'game'

urlpatterns = [
    path('', views.index, name='home'),
    path('instructions/', views.instructions, name='instructions'),
    path('gamepage/', views.gamepage, name='gamepage'),
    path('policymaking/', views.policy, name='policy'),
    path('staticpage/', views.staticpage, name='staticpage'),
    path('newspage/', views.newspage, name='newspage'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)