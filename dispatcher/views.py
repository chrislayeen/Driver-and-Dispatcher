from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from driver.models import Inspection, Issue, Trip, Notification
from dispatcher.models import DispatcherNote


def dispatcher_dashboard(request):
    pending_inspections = Inspection.objects.filter(review_status='pending').order_by('-submitted_at')
    pending_count = pending_inspections.count()
    
    open_issues = Issue.objects.filter(status='open').order_by('-submitted_at')
    issue_count = open_issues.count()
    
    active_trips = Trip.objects.filter(status='in_progress').count()
    
    from django.utils import timezone
    today = timezone.now().date()
    completed_today = Trip.objects.filter(status='completed', started_at__date=today).count()
    
    context = {
        'pending_count': pending_count,
        'open_issues': issue_count,
        'active_trips': active_trips,
        'completed_today': completed_today,
        'recent_inspections': pending_inspections[:5],
        'recent_issues': open_issues[:5],
    }
    return render(request, 'dispatcher/dashboard.html', context)


def approvals(request):
    inspections = Inspection.objects.select_related('trip').order_by('-submitted_at')
    return render(request, 'dispatcher/approvals.html', {'inspections': inspections})


def approve_inspection(request, pk):
    if request.method == 'POST':
        inspection = get_object_or_404(Inspection, pk=pk)
        action = request.POST.get('action')  # 'approved' or 'rejected'
        note_text = request.POST.get('note', '')
        inspection.review_status = action
        inspection.save()

        # Robust Trip Promotion: Update trip status if this is a pre/post-inspection approval
        if action == 'approved':
            if inspection.inspection_type == 'pre':
                trip = inspection.trip
                if trip:
                    trip.status = 'in_progress'
                    trip.save()
            elif inspection.inspection_type == 'post':
                trip = inspection.trip
                if trip:
                    trip.status = 'completed'
                    trip.save()

        # Create notification for driver
        Notification.objects.create(
            title=f"Inspection {action.capitalize()}",
            message=f"Your {inspection.get_inspection_type_display()} was {action} by dispatch.",
            trip=inspection.trip
        )

        DispatcherNote.objects.create(
            inspection_id=pk,
            note=note_text,
            action=action
        )
        return JsonResponse({'success': True, 'status': action})
    return JsonResponse({'success': False}, status=400)


def incidents(request):
    issues = Issue.objects.select_related('trip').order_by('-submitted_at')
    return render(request, 'dispatcher/incidents.html', {'issues': issues})


def resolve_issue(request, pk):
    if request.method == 'POST':
        issue = get_object_or_404(Issue, pk=pk)
        issue.status = 'resolved'
        issue.save()

        # Create notification for driver
        Notification.objects.create(
            title="Issue Resolved",
            message=f"Issue '{issue.description[:20]}...' has been marked as resolved.",
            trip=issue.trip
        )

        DispatcherNote.objects.create(
            issue_id=pk,
            note=request.POST.get('note', ''),
            action='resolve'
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
