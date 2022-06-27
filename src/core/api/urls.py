from django.urls import path
from core.api import views as core_views


app_name = 'core'

urlpatterns = [
    path('register/', core_views.RegisterView.as_view(), name='register'),
    path('me/', core_views.MeDetailView.as_view(), name='me'),

    # List all users
    path('users/', core_views.ListUsersView.as_view(), name='users'),

    # Update user
    path('user/<user_uuid>/', core_views.UpdateUserView.as_view(), name='update_user'),

    # Create appointment
    path('new_appointment/', core_views.CreateAppointmentView.as_view(), name='new_appointment'),
]
