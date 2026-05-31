from django.urls import path
from django.shortcuts import redirect
from . import views

def root_redirect(request):
    if 'user_id' in request.session:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    path('', root_redirect, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]
