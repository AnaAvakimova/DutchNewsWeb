from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_news, name='main'),
    path('<int:num>/', views.get_article, name='news')
]
