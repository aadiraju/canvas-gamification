from rest_framework import serializers

from video_recommendations.models import UserVideoJunction


class UserVideoJunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideoJunction
        fields = ['user', 'video', 'rating']
