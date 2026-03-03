from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def role_select(request):
    return render(request, 'role_select.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', role_select, name='role_select'),
    path('driver/', include('driver.urls')),
    path('dispatcher/', include('dispatcher.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
