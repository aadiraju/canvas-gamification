from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand

from googleapiclient.discovery import build
import os

from course.models.models import QuestionCategory
from video_recommendations.models import Video


def get_videos_by_category_name(category_name):
    service = build('youtube', 'v3', developerKey=os.environ['YOUTUBE_API_KEY'])

    search_query = category_name + 'in Java'
    response = service.search().list(
        part="id",
        type='video',
        q=search_query,
        order='relevance',
        maxResults=10).execute()

    videos = []
    for result in response['items']:
        videos.append(result['id']['videoId'])

    for video_id in videos:
        video_data = service.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id,
            fields='items(snippet,statistics,contentDetails(duration))').execute()
        video_data = video_data['items'][0]

        title = video_data['snippet']['title']
        description = video_data['snippet']['description']
        duration = video_data['contentDetails']['duration']
        published_at = video_data['snippet']['publishedAt']
        view_count = video_data['statistics']['viewCount']
        like_count = video_data['statistics']['likeCount']
        comment_count = video_data['statistics']['commentCount']
        youtube_category = video_data['snippet']['categoryId']
        try:
            associated_category = QuestionCategory.objects.get(name=category_name)
        except ObjectDoesNotExist:
            associated_category = None

        try:
            new_video = Video(video_id=video_id, title=title, description=description, duration=duration,
                              publish_date=published_at, view_count=view_count, like_count=like_count,
                              comment_count=comment_count, youtube_category=youtube_category,
                              associated_category=associated_category)
            new_video.save()
        except ValidationError:
            pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Updating DB with Youtube Videos')
        get_videos_by_category_name('Variables')
