
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    # API endpoints for operations (cotisations, prets, remboursements)
    path('api/operations/', include('apps.operations.urls')),
]
