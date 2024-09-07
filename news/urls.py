from django.urls import path
from . import views

urlpatterns = [
    # path('', views.get_main, name='main'),
    path('', views.get_news, name='news'),
    path('news/<int:num>/', views.get_article, name='article'),
    path('disclaimer/', views.get_disclaimer, name='disclaimer')
]
