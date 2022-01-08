from rest_framework import viewsets

from api.serializers import VideoSerializer
from video_recommendations.models import Video


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
