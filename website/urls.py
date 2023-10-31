from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('details/<int:id>/', views.details, name='details'),
    path('rate/<int:id>/', views.rate_junior, name='rate_junior'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('joinus/', views.joinus, name='joinus'),
]

