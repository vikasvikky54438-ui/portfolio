
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Transactions
    path(
        'edit/<int:id>/',
        views.edit_transaction,
        name='edit_transaction'
    ),

    path(
        'delete/<int:id>/',
        views.delete_transaction,
        name='delete_transaction'
    ),
]
