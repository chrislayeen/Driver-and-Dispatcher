from django.contrib import admin
from .models import Trip, Inspection, InspectionPhoto, Issue, IssuePhoto

class InspectionPhotoInline(admin.TabularInline):
    model = InspectionPhoto
    extra = 0

class IssuePhotoInline(admin.TabularInline):
    model = IssuePhoto
    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver_name', 'trailer_id', 'status', 'started_at']
    list_filter = ['status']

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'inspection_type', 'trip', 'review_status', 'submitted_at']
    list_filter = ['inspection_type', 'review_status']
    inlines = [InspectionPhotoInline]

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'severity', 'status', 'trip', 'submitted_at']
    list_filter = ['severity', 'status']
    inlines = [IssuePhotoInline]
