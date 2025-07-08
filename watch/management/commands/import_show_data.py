import json

from django.core.management.base import BaseCommand

from watch.fetch.fetch import fetch_json_data
from watch.tasks import process_single_show

shows_json_url = "https://channelsapi.s3.amazonaws.com/media/test/shows.json"


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with open("watch/fetched_data/shows.json", "r") as file:
                shows = json.load(file)
        except FileNotFoundError:
            # Create the file and populate it with data
            fetch_json_data(shows_json_url, shows)  # type: ignore

            with open("watch/fetched_data/shows.json", "r") as file:
                shows = json.load(file)

        for show in shows:
            show_data = {
                "show": show,
                "name": show["name"],
                "imdb_rating": show["imdb_rating"],
                "image": show["image"],
                "description": show["description"],
                "release_date": show["first_aired"],
            }

            process_single_show.delay(show_data)  # type: ignore
