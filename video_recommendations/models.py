from django.db import models

from accounts.models import MyUser


class Video(models.Model):
    video_id = models.CharField(max_length=11, null=False, blank=True, primary_key=True)
    title = models.TextField(db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.video_id


class UserVideoJunction(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='video_junctions', db_index=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='user_junctions', db_index=True)
    rating = models.IntegerField(null=True)

    class Meta:
        unique_together = ('user', 'video')