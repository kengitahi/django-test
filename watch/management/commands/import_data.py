import json

from django.core.management.base import BaseCommand

from watch.fetch.fetch import fetch_json_data
from watch.models import Movie, Show

movies_json_url = "https://channelsapi.s3.amazonaws.com/media/test/movies.json"
shows_json_url = "https://channelsapi.s3.amazonaws.com/media/test/shows.json"


class Command(BaseCommand):
    def get_sources(self, production):
        sources = set()
        all_sources = production.get("modes", {}).get("web_sources", {})
        source_categories = ["ppv", "authenticated", "free", "subscriptions"]

        for category in source_categories:
            category_sources = all_sources.get(category, [])

            for source in category_sources:
                source_name = source.get("name")

                if source_name:
                    # Add to set to ensure uniqueness
                    sources.add(source_name)

        # Return list
        return list(sources)

    def handle(self, *args, **options):
        try:
            with open("watch/fetched_data/movies.json", "r") as file:
                movies = json.load(file)
        except FileNotFoundError:
            # Create the file and populate it with data
            fetch_json_data(movies_json_url, movies)

            with open("watch/fetched_data/movies.json", "r") as file:
                movies = json.load(file)

        for movie in movies:
            sources_list = self.get_sources(movie)
            # Fetch kinopoisk rating here

            movie_data = {
                "name": movie["name"],
                "imdb_rating": movie["imdb_rating"],
                "image": movie["image"],
                "description": movie["description"],
                "release_year": movie["release_year"],
                "sources": sources_list,
            }

            movie_instance = Movie.objects.create(
                name=movie_data["name"],
                imdb_rating=movie_data["imdb_rating"],
                image=movie_data["image"],
                description=movie_data["description"],
                release_year=movie_data["release_year"],
                sources_list=movie_data["sources"],
            )

            print(movie_instance)

        try:
            with open("watch/fetched_data/shows.json", "r") as file:
                shows = json.load(file)
        except FileNotFoundError:
            # Create the file and populate it with data
            fetch_json_data(shows_json_url, shows)

            with open("watch/fetched_data/shows.json", "r") as file:
                shows = json.load(file)

        for show in shows:
            sources_list = self.get_sources(show)
            # Fetch kinopoisk rating here

            show_data = {
                "name": show["name"],
                "imdb_rating": show["imdb_rating"],
                "image": show["image"],
                "description": show["description"],
                "release_date": show["first_aired"],
                "sources": sources_list,
            }

            show_instance = Show.objects.create(
                name=show_data["name"],
                imdb_rating=show_data["imdb_rating"],
                image=show_data["image"],
                description=show_data["description"],
                release_date=show_data["release_date"],
                sources_list=show_data["sources"],
            )

            print(show_instance)
