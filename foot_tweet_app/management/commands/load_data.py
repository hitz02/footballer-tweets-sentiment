import csv
from django.core.management import BaseCommand
from foot_tweet_app.models import Twitter_Handles

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):

        self.stdout.write("Starting to delete previous data from database")
        t = Twitter_Handles.objects.all()
        t._raw_delete(t.db)
        self.stdout.write("Previous data deleted Successfully")

        path = kwargs['path']
        with open(path, 'rt', encoding='Latin1') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader, None)
            for row in reader:
                team_data = Twitter_Handles.objects.create(
                    player_name=row[0].strip(),
                    twitter_handle=row[1].strip(),
                    team_name=row[2].strip(),
                    player_position=row[3].strip()
                )