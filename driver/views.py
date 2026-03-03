from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import models

from .models import Trip, Inspection, InspectionPhoto, Issue, IssuePhoto, Notification
from .forms import PreInspectionForm, PostInspectionForm, IssueForm


def get_notifications(request):
    """Returns unread notifications. In this demo, we filter by session's trip or recent."""
    trip_id = request.session.get('trip_id')
    if trip_id:
        # Show notifications for current trip + any "global" (null trip) ones
        notifications = Notification.objects.filter(models.Q(trip_id=trip_id) | models.Q(trip__isnull=True), is_read=False)
    else:
        notifications = Notification.objects.filter(is_read=False)[:5]

    data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'created_at': n.created_at.strftime('%H:%M'),
        } for n in notifications
    ]
    return JsonResponse({'notifications': data, 'unread_count': len(data)})


def mark_notification_read(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def driver_home(request):
    trip_id = request.session.get('trip_id')
    trip = None
    if trip_id:
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            trip = None

    # Dashboard Stats
    from django.utils import timezone
    today = timezone.now().date()
    
    completed_today = Trip.objects.filter(status='completed', started_at__date=today).count()
    open_issues = Issue.objects.filter(status='open').count()
    recent_notifications = Notification.objects.filter(is_read=False)[:3]
    
    # Dynamic Greeting
    hour = timezone.now().hour
    if hour < 12: greeting = "Good Morning"
    elif hour < 17: greeting = "Good Afternoon"
    else: greeting = "Good Evening"

    context = {
        'trip': trip,
        'completed_today': completed_today,
        'open_issues': open_issues,
        'recent_notifications': recent_notifications,
        'greeting': greeting,
        'now': timezone.now(),
    }
    return render(request, 'driver/home.html', context)


def pre_inspection(request):
    if request.method == 'POST':
        form = PreInspectionForm(request.POST)
        if form.is_valid():
            trip_id = request.session.get('trip_id')
            if not trip_id:
                trip = Trip.objects.create(driver_name='Driver', status='pending')
                request.session['trip_id'] = trip.id
            else:
                trip = get_object_or_404(Trip, id=trip_id)

            inspection = form.save(commit=False)
            inspection.trip = trip
            inspection.inspection_type = 'pre'
            inspection.save()

            for f in request.FILES.getlist('photos'):
                InspectionPhoto.objects.create(inspection=inspection, image=f)

            # Store inspection ID in session so we can poll it
            request.session['pending_inspection_id'] = inspection.id

            # Return JSON — the AJAX handler on the page will show the waiting overlay
            return JsonResponse({'success': True, 'inspection_pk': inspection.id})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = PreInspectionForm()
    return render(request, 'driver/pre_inspection.html', {'form': form})


def inspection_status(request, pk):
    """Polling endpoint: returns the current review_status of an inspection."""
    inspection = get_object_or_404(Inspection, pk=pk)
    return JsonResponse({'review_status': inspection.review_status})


def in_progress(request):
    trip_id = request.session.get('trip_id')
    trip = None
    if trip_id:
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            pass

    # Update trip to in_progress once pre-inspection is approved
    insp_id = request.session.get('pending_inspection_id')
    if insp_id and trip and trip.status != 'in_progress':
        try:
            insp = Inspection.objects.get(id=insp_id, review_status='approved')
            trip.status = 'in_progress'
            trip.save()
        except Inspection.DoesNotExist:
            pass

    return render(request, 'driver/in_progress.html', {'trip': trip})


def post_inspection(request):
    if request.method == 'POST':
        form = PostInspectionForm(request.POST)
        if form.is_valid():
            trip_id = request.session.get('trip_id')
            trip = None
            if trip_id:
                try:
                    trip = Trip.objects.get(id=trip_id)
                except Trip.DoesNotExist:
                    pass

            inspection = form.save(commit=False)
            inspection.trip = trip
            inspection.inspection_type = 'post'
            inspection.save()

            for f in request.FILES.getlist('photos'):
                InspectionPhoto.objects.create(inspection=inspection, image=f)

            # Store post-inspection ID for polling
            request.session['pending_post_inspection_id'] = inspection.id

            return JsonResponse({'success': True, 'inspection_pk': inspection.id})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = PostInspectionForm()
    return render(request, 'driver/post_inspection.html', {'form': form})


def post_inspection_complete(request):
    """Called by driver after post-inspection is approved — clears the trip."""
    trip_id = request.session.get('trip_id')
    if trip_id:
        try:
            trip = Trip.objects.get(id=trip_id)
            trip.status = 'completed'
            trip.save()
        except Trip.DoesNotExist:
            pass
    request.session.pop('trip_id', None)
    request.session.pop('pending_inspection_id', None)
    request.session.pop('pending_post_inspection_id', None)
    return JsonResponse({'success': True})


def submit_issue(request):
    """AJAX endpoint for reporting an issue during a trip."""
    if request.method == 'POST':
        form = IssueForm(request.POST)
        trip_id = request.session.get('trip_id')
        trip = None
        if trip_id:
            try:
                trip = Trip.objects.get(id=trip_id)
            except Trip.DoesNotExist:
                pass

        if form.is_valid():
            issue = form.save(commit=False)
            issue.trip = trip
            issue.save()

            for f in request.FILES.getlist('photos'):
                IssuePhoto.objects.create(issue=issue, image=f)

            return JsonResponse({'success': True, 'issue_id': issue.id})
        else:
            return JsonResponse({'success': False, 'errors': str(form.errors)})
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
