from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from googleapiclient.discovery import build
import os

from course.models.models import QuestionCategory
from video_recommendations.models import Video


def get_videos_by_category_name(category_name, category_id):
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

        title = video_data['snippet'].get('title', '')
        description = video_data['snippet'].get('description', None)
        duration = video_data['contentDetails'].get('duration', None)
        published_at = video_data['snippet'].get('publishedAt', None)
        view_count = video_data['statistics'].get('viewCount', None)
        like_count = video_data['statistics'].get('likeCount', None)
        comment_count = video_data['statistics'].get('commentCount', None)
        youtube_category = video_data['snippet'].get('categoryId', None)
        try:
            associated_category = QuestionCategory.objects.get(description=category_id)
        except ObjectDoesNotExist:
            associated_category = None

        try:
            existing_video = Video.objects.get(video_id=video_id)
            existing_video.associated_categories.add(category_id)
        except ObjectDoesNotExist:
            try:
                new_video = Video(video_id=video_id, title=title, description=description, duration=duration,
                                  publish_date=published_at, view_count=view_count, like_count=like_count,
                                  comment_count=comment_count, youtube_category=youtube_category)
                new_video.save()
                new_video.associated_categories.add(category_id)
            except (ValidationError, IntegrityError):
                pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Updating DB with Youtube Videos')
        sub_categories = QuestionCategory.objects.exclude(parent=None)
        ids = [21, 32, 34]
        for subcat in sub_categories:
            if subcat.pk in ids:
                print('Querying ' + subcat.description + '...')
                get_videos_by_category_name(subcat.description, subcat.pk)
