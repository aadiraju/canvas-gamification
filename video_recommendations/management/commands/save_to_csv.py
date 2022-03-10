import pandas as pd
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from googleapiclient.discovery import build
import os

from course.models.models import QuestionCategory
from video_recommendations.models import Video


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--filepath', type=str)

    def handle(self, *args, **options):
        filepath = options['filepath']
        print(f'Saving CSV of videos to {filepath}')
        df = pd.DataFrame(list(Video.objects.all().values()))
        categories = []
        for obj in Video.objects.all():
            categories.append(', '.join([c.name for c in obj.associated_categories.all()]))
        df['categories'] = categories
        df.to_csv(filepath, index=False)
