from django.urls import path
from . import views #dot for same folder
from .views import CustomLoginView, CustomPasswordChangeView
from django.contrib.auth.views import LogoutView,  PasswordChangeDoneView

urlpatterns = [
    
    # Authentication-related paths
    path('', CustomLoginView.as_view(template_name='login.html'), name='login'),  # Path for user login
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Logout view
    
    # Dashboard paths
    path('clients/', views.list_clients, name='list_clients'),  # Path for the admin/team dashboard
    path('reports/<int:client_id>/', views.view_client_reports, name='view_client_reports'),  # Path for the client dashboard
    path('export_reports/<str:format>/', views.export_reports, name='export_reports'),

    # Integrations
    path("webhook/zapier/", views.zapier_webhook, name="zapier_webhook"),
]
