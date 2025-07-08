import json

from django.core.management.base import BaseCommand

from watch.fetch.fetch import fetch_json_data
from watch.tasks import process_single_movie

movies_json_url = "https://channelsapi.s3.amazonaws.com/media/test/movies.json"


class Command(BaseCommand):
    def handle(self):
        try:
            with open("watch/fetched_data/movies.json", "r") as file:
                movies = json.load(file)
        except FileNotFoundError:
            # Create the file and populate it with data
            fetch_json_data(movies_json_url, movies)  # type: ignore

            with open("watch/fetched_data/movies.json", "r") as file:
                movies = json.load(file)

        for movie in movies:
            movie_data = {
                "movie": movie,
                "name": movie["name"],
                "imdb_rating": movie["imdb_rating"],
                "image": movie["image"],
                "description": movie["description"],
                "release_year": movie["release_year"],
            }

            process_single_movie.delay(movie_data) # type: ignore
