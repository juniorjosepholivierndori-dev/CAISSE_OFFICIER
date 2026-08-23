import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import Notification, Operation, OperationPerso


def operation_payload(operation):
    return {
        "id": operation.id,
        "type": operation.type,
        "type_label": operation.get_type_display(),
        "description": operation.description,
        "amount": operation.amount,
        "status": operation.status,
        "status_label": operation.get_status_display(),
        "date": operation.operation_date.isoformat(),
    }


@login_required
@require_GET
def member_dashboard_api(request):
    operations = Operation.objects.filter(member=request.user)
    validated_cotisations = operations.filter(
        type=Operation.Type.COTISATION,
        status=Operation.Status.VALIDATED,
    )
    pending_count = operations.filter(status=Operation.Status.PENDING).count()
    validated_loans = operations.filter(
        type=Operation.Type.PRET,
        status=Operation.Status.VALIDATED,
    )
    validated_repayments = operations.filter(
        type=Operation.Type.REMBOURSEMENT,
        status=Operation.Status.VALIDATED,
    )
    profile = getattr(request.user, "member_profile", None)

    return JsonResponse({
        "member": {
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "matricule": profile.matricule if profile else "",
            "grade": profile.grade if profile else "",
            "unite": profile.unite if profile else "",
            "telephone": profile.telephone if profile else "",
        },
        "stats": {
            "cotisations_versees": sum(item.amount for item in validated_cotisations),
            "prets_en_cours": operations.filter(type=Operation.Type.PRET, status=Operation.Status.PENDING).count(),
            "demandes_en_attente": pending_count,
            "cotisations_enregistrees": validated_cotisations.count(),
            "prets_obtenus": validated_loans.count(),
            "remboursements_effectues": validated_repayments.count(),
            "solde_disponible": sum(item.amount for item in validated_cotisations)
            - sum(item.amount for item in validated_loans),
        },
        "operations": [operation_payload(item) for item in operations[:20]],
    })


@login_required
@require_POST
def create_member_request(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Le corps de la requête doit être un JSON valide."}, status=400)

    operation_type = payload.get("type")
    description = str(payload.get("description", "")).strip()
    amount = payload.get("amount")

    valid_types = {choice.value for choice in Operation.Type}
    if operation_type not in valid_types:
        return JsonResponse({"detail": "Le type de demande est invalide."}, status=400)
    if not description:
        return JsonResponse({"detail": "La description est obligatoire."}, status=400)
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return JsonResponse({"detail": "Le montant doit être un nombre entier."}, status=400)
    if amount <= 0:
        return JsonResponse({"detail": "Le montant doit être supérieur à zéro."}, status=400)

    adherent = getattr(request.user, "adherent", None)
    operation = Operation.objects.create(
        member=request.user,
        adherent=adherent,
        type=operation_type,
        description=description,
        amount=amount,
        operation_date=date.today(),
    )
    if adherent:
        OperationPerso.objects.create(
            operation=operation,
            adherent=adherent,
            utilisateur=request.user,
        )
    Notification.objects.create(
        member=request.user,
        title="Nouvelle demande enregistrée",
        description=f"Votre demande de {amount:,} FCFA est en attente de validation.",
    )
    return JsonResponse({"operation": operation_payload(operation)}, status=201)


@login_required
@require_GET
def member_notifications_api(request):
    notifications = Notification.objects.filter(member=request.user)[:30]
    return JsonResponse({
        "notifications": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "is_read": item.is_read,
                "created_at": item.created_at.isoformat(),
            }
            for item in notifications
        ]
    })
