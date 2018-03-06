from django.conf.urls import url

from exploration import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^save/', views.save, name='save'),
]
