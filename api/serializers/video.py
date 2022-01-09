from rest_framework import serializers

from video_recommendations.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'title', 'description', 'duration', 'publish_date', 'view_count', 'like_count',
                  'youtube_category', 'associated_category']
