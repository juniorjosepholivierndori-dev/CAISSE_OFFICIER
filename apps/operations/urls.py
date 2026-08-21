from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CotisationViewSet, PretViewSet, RemboursementViewSet, DashboardAPIView

router = DefaultRouter()
router.register(r'cotisations', CotisationViewSet, basename='cotisation')
router.register(r'prets', PretViewSet, basename='pret')
router.register(r'remboursements', RemboursementViewSet, basename='remboursement')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardAPIView.as_view(), name='operations-dashboard'),
]
