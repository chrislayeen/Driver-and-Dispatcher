from django.urls import path
from . import views

app_name = 'dispatcher'

urlpatterns = [
    path('', views.dispatcher_dashboard, name='dashboard'),
    path('approvals/', views.approvals, name='approvals'),
    path('approvals/<int:pk>/action/', views.approve_inspection, name='approve_inspection'),
    path('incidents/', views.incidents, name='incidents'),
    path('incidents/<int:pk>/resolve/', views.resolve_issue, name='resolve_issue'),
]
