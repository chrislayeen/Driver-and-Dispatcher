from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from driver.models import Inspection, Issue, Trip
from dispatcher.models import DispatcherNote


def dispatcher_dashboard(request):
    pending_count = Inspection.objects.filter(review_status='pending').count()
    open_issues = Issue.objects.filter(status='open').count()
    return render(request, 'dispatcher/dashboard.html', {
        'pending_count': pending_count,
        'open_issues': open_issues,
    })


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
        DispatcherNote.objects.create(
            issue_id=pk,
            note=request.POST.get('note', ''),
            action='resolve'
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
