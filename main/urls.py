from django.urls import path, include
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.loginUser, name='login'),
    path('create_user/', views.createUser, name='create_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutUser, name='logout'), 
    path('settings/', views.settings, name="settings"),
    path('delete_user/<str:pk>/', views.deleteUser, name="delete_user"),
    path('change_password/', views.changePassword, name="change_password"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="main/password_reset.html", email_template_name='main/password_reset_email.html'), name="password_reset"),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name="main/password_reset_done.html"), name="password_reset_done"),
    path('reset_password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="main/password_reset_complete.html"), name="password_reset_complete"),
    path('verify_email/', include(email_urls)),
    path('create_issue/', views.createIssue, name='create_issue'),
    path('update_issue/<str:pk>/', views.updateIssue, name="update_issue"),
    path('delete_issue/<str:pk>/', views.deleteIssue, name="delete_issue"),
    path('archive/', views.archive, name="archive"),
    path('statistics/', views.statistics, name="statistics"),
]
