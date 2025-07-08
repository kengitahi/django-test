import asyncio

from celery import shared_task
from kinopoisk import KPClient

from .models import Movie, Show

KINOPOSK_API_KEY = "4cb0d1a1-46a0-4cf2-86a3-8321e4e5fdc5"  # TODO: Bad practice


def get_sources(production):
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


@shared_task
async def fetch_kinopoisk_rating(keyword):
    """
    API task to get the kinopoisk rating for a single movie or TV show
    """
    client = KPClient(KINOPOSK_API_KEY)

    production = await client.search_movie(keyword)

    if (
        not production
        or production[0] is None
        or production[0].raiting.kinopoisk is None
    ):
        return 1.0

    return production[0].raiting.kinopoisk.value


@shared_task
def process_single_movie(movie_data):
    """
    Celery task to process a single movie, fetch its Kinopoisk rating, get its sources list and save it to the database.
    """

    print(f"Processing movie: {movie_data['name']}")

    kinopoisk_rating = asyncio.run(fetch_kinopoisk_rating(movie_data["name"])) or 1.0
    sources_list = get_sources(movie_data["movie"])

    movie_instance = Movie.objects.create(
        name=movie_data["name"],
        imdb_rating=movie_data["imdb_rating"],
        kinopoisk_rating=kinopoisk_rating,
        image=movie_data["image"],
        description=movie_data["description"],
        release_year=movie_data["release_year"],
        sources_list=sources_list,
    )

    print(
        f"Processed movie: {movie_instance.name} with Kinopoisk rating: {kinopoisk_rating}"
    )


@shared_task
def process_single_show(show_data):
    """
    Celery task to process a single show, fetch its Kinopoisk rating, get its sources list and save it to the database.
    """

    print(f"Processing show: {show_data['name']}")

    kinopoisk_rating = asyncio.run(fetch_kinopoisk_rating(show_data["name"])) or 1.0
    sources_list = get_sources(show_data["show"])

    show_instance = Show.objects.create(
        name=show_data["name"],
        imdb_rating=show_data["imdb_rating"],
        kinopoisk_rating=kinopoisk_rating,
        image=show_data["image"],
        description=show_data["description"],
        release_date=show_data["release_date"],
        sources_list=sources_list,
    )

    print(
        f"Processed movie: {show_instance.name} with Kinopoisk rating: {kinopoisk_rating}"
    )


@shared_task
def fetch_seasons(show_name):
    """
    Celery task to fetch the seasons for a single show.
    """
    client = KPClient(KINOPOSK_API_KEY)

    show = asyncio.run(client.search_movie(show_name))
    seasons = asyncio.run(client.get_seasons_data(show[0].id.kinopoisk))

    return seasons


@shared_task
def fetch_episodes(show_name, season_number):
    """
    Celery task to fetch the episodes for a single season.
    """
    seasons = asyncio.run(fetch_seasons(show_name))
    episodes = []

    for season in seasons[:season_number]:
        for index, episode in enumerate(season, start=1):
            episodes.append(
                {
                    "episode_number": index,
                    "name": episode.name.en,
                },
            )

    return episodes


if __name__ == "__main__":
    # Example usage

    # async def main():
    #     seasons = await fetch_seasons("Game of Thrones")
    #     print(seasons)

    fetch_episodes("Game of Thrones", 1)
