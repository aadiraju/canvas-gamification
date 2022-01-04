from rest_framework import viewsets

from api.serializers import UserVideoJunctionSerializer
from video_recommendations.models import UserVideoJunction


class UserVideoJunctionViewSet(viewsets.ModelViewSet):
    queryset = UserVideoJunction.objects.all()
    serializer_class = UserVideoJunctionSerializer
