from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profil_tresorier(request):
    user = request.user

    if user.role != user.Role.TRESORIER:
        return Response(
            {"detail": "Accès réservé au trésorier."},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response({
        "id": user.id,
        "username": user.username,
        "nom": user.last_name,
        "prenom": user.first_name,
        "email": user.email,
        "role": user.get_role_display(),
    })