from django.db import models

# Dispatcher app proxies / admin views for the same models
# Dispatcher queries from driver.models via cross-app imports

class DispatcherNote(models.Model):
    """Notes added by dispatcher during approval/resolve actions."""
    inspection_id = models.IntegerField(null=True, blank=True)
    issue_id = models.IntegerField(null=True, blank=True)
    note = models.TextField()
    action = models.CharField(max_length=20)  # approve, reject, resolve
    actioned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DispatcherNote [{self.action}]"
