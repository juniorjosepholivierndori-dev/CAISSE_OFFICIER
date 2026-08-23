from django.urls import path

from .api import create_member_request, member_dashboard_api, member_notifications_api

app_name = "operations"

urlpatterns = [
    path("dashboard/", member_dashboard_api, name="member-dashboard"),
    path("requests/", create_member_request, name="member-request"),
    path("notifications/", member_notifications_api, name="member-notifications"),
]
