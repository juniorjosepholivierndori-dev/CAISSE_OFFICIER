from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count

from .models import Cotisation, Pret, Remboursement
from .serializers import CotisationSerializer, PretSerializer, RemboursementSerializer


class CotisationViewSet(viewsets.ModelViewSet):
    queryset = Cotisation.objects.all().select_related('membre')
    serializer_class = CotisationSerializer
    permission_classes = [permissions.IsAuthenticated]


class PretViewSet(viewsets.ModelViewSet):
    queryset = Pret.objects.all().select_related('emprunteur')
    serializer_class = PretSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_pret = Pret.objects.aggregate(total=Sum('montant'))['total'] or 0
        en_cours = Pret.objects.filter(statut='EN_COURS').count()
        return Response({'total_pret': total_pret, 'prets_en_cours': en_cours})


class RemboursementViewSet(viewsets.ModelViewSet):
    queryset = Remboursement.objects.all().select_related('pret')
    serializer_class = RemboursementSerializer
    permission_classes = [permissions.IsAuthenticated]


# A small dashboard viewset for totals
from rest_framework.views import APIView

class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_cotisations = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
        nb_cotisations = Cotisation.objects.count()
        total_prets = Pret.objects.aggregate(total=Sum('montant'))['total'] or 0
        prets_en_cours = Pret.objects.filter(statut='EN_COURS').count()
        nb_users = request.user.__class__.objects.count()
        return Response({
            'nb_users': nb_users,
            'total_cotisations': total_cotisations,
            'nb_cotisations': nb_cotisations,
            'total_prets': total_prets,
            'prets_en_cours': prets_en_cours,
        })