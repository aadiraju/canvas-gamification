from django.core.management.base import BaseCommand

# from googleapiclient.discovery import build
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Updating DB with Youtube Videos')
        print(os.environ['YOUTUBE_API_KEY'])
