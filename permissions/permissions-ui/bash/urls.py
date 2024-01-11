from django.urls import path
#from .views import HomePageView
from . import views
app_name = 'bash'

urlpatterns = [
    path('', views.bash_view, name='index'),
    path('public', views.public_view, name='public'),
    path('registered', views.registered_view, name='registered'),
    path('controlled', views.controlled_view, name='controlled')
]