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

    kinopoisk_rating = asyncio.run(fetch_kinopoisk_rating(movie_data["name"])) or 1.0
    sources_list = get_sources(movie_data["movie"])

    Movie.objects.create(
        name=movie_data["name"],
        imdb_rating=movie_data["imdb_rating"],
        kinopoisk_rating=kinopoisk_rating,
        image=movie_data["image"],
        description=movie_data["description"],
        release_year=movie_data["release_year"],
        sources_list=sources_list,
    )


@shared_task
def process_single_show(show_data):
    """
    Celery task to process a single show, fetch its Kinopoisk rating, get its sources list and save it to the database.
    """

    kinopoisk_rating = asyncio.run(fetch_kinopoisk_rating(show_data["name"])) or 1.0
    sources_list = get_sources(show_data["show"])

    Show.objects.create(
        name=show_data["name"],
        imdb_rating=show_data["imdb_rating"],
        kinopoisk_rating=kinopoisk_rating,
        image=show_data["image"],
        description=show_data["description"],
        release_date=show_data["release_date"],
        sources_list=sources_list,
    )


@shared_task
def fetch_seasons(show_name):
    """
    Celery task to fetch the seasons for a single show.
    """
    client = KPClient(KINOPOSK_API_KEY)

    show = asyncio.run(client.search_movie(show_name))
    seasons = asyncio.run(client.get_seasons_data(show[0].id.kinopoisk))

    seasons_data = []

    for season in seasons:
        seasons_data.append(
            {
                "show": show_name,
                "season_number": season.number,
            },
        )

    return seasons_data


@shared_task
def fetch_episodes(show_name, season_number):
    """
    Celery task to fetch the episodes for a single season.
    """
    client = KPClient(KINOPOSK_API_KEY)

    show = asyncio.run(client.search_movie(show_name))
    seasons = asyncio.run(client.get_seasons_data(show[0].id.kinopoisk))

    episodes = []
    episodes_data = []

    for season in seasons:
        if season.number == season_number:
            episodes = season.episodes or []

    if not episodes:
        return []

    for episode in episodes:
        episodes_data.append(
            {
                "episode_number": episode.number,
                "name": episode.name.en,
            },
        )

    return episodes_data


if __name__ == "__main__":
    # Example usage
    from watch.models import Movie, Show

    fetch_seasons("Game of Thrones")

    # fetch_episodes("Game of Thrones", 1)
