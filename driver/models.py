from django.db import models

class Trip(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    driver_name = models.CharField(max_length=100, default='Driver')
    trailer_id = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.id} — {self.driver_name} ({self.status})"


class Inspection(models.Model):
    TYPE_CHOICES = [('pre', 'Pre-Trip'), ('post', 'Post-Trip')]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='inspections', null=True, blank=True)
    inspection_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='pre')
    brakes_ok = models.BooleanField(default=False)
    tires_ok = models.BooleanField(default=False)
    fluids_ok = models.BooleanField(default=False)
    lug_nuts_ok = models.BooleanField(default=False)
    shocks_ok = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    REVIEW_STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    review_status = models.CharField(max_length=10, choices=REVIEW_STATUS, default='pending')

    def __str__(self):
        return f"{self.get_inspection_type_display()} — Trip {self.trip_id}"


class InspectionPhoto(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='inspections/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Inspection {self.inspection_id}"


class Issue(models.Model):
    SEVERITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('open', 'Open'), ('resolved', 'Resolved')]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='issues', null=True, blank=True)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue [{self.severity.upper()}] — {self.description[:40]}"


class IssuePhoto(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='issues/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Issue {self.issue_id}"


class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Associated trip for context
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.created_at.strftime('%Y-%m-%d %H:%M')}"
