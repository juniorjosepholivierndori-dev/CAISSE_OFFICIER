from rest_framework import serializers
from .models import Cotisation, Pret, Remboursement
from django.conf import settings


class CotisationSerializer(serializers.ModelSerializer):
    membre_email = serializers.EmailField(source='membre.email', read_only=True)

    class Meta:
        model = Cotisation
        fields = ('id', 'membre', 'membre_email', 'montant', 'date', 'type_cotisation', 'note')


class PretSerializer(serializers.ModelSerializer):
    emprunteur_email = serializers.EmailField(source='emprunteur.email', read_only=True)

    class Meta:
        model = Pret
        fields = ('id', 'emprunteur', 'emprunteur_email', 'montant', 'taux_annuel', 'date_debut', 'duree_mois', 'solde_restant', 'statut')


class RemboursementSerializer(serializers.ModelSerializer):
    pret_id = serializers.IntegerField(source='pret.id', read_only=True)

    class Meta:
        model = Remboursement
        fields = ('id', 'pret', 'pret_id', 'montant', 'date', 'note')