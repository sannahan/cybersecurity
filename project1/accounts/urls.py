from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('secret/', views.secret, name='secret'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('cards/', views.cards, name='cards'),
    path('message/', views.message, name='message'),
    path('error/', views.error, name='error')
]