from django.urls import path
from accounts.views import*

urlpatterns = [
    path('',MainHome.as_view()),
    path('reg/',Registration.as_view(),name='reg'),
    path('log/',Login.as_view(),name='log'),
    path('lgout/',Login.as_view(),name='logout'),
]
