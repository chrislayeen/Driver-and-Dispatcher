from django.urls import path
from . import views

app_name = 'driver'

urlpatterns = [
    path('scanner/', views.scanner_view, name='scanner'),
    path('trailer-auth/', views.trailer_verification_view, name='trailer_verification'),
    path('', views.driver_home, name='home'),
    path('pre-inspection/', views.pre_inspection, name='pre_inspection'),
    path('in-progress/', views.in_progress, name='in_progress'),
    path('post-inspection/', views.post_inspection, name='post_inspection'),
    path('post-inspection/complete/', views.post_inspection_complete, name='post_inspection_complete'),
    path('inspection-status/<int:pk>/', views.inspection_status, name='inspection_status'),
    path('submit-issue/', views.submit_issue, name='submit_issue'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
]
