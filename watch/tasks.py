import asyncio

from celery import shared_task
from kinopoisk import KPClient

# from .models import Movie, Show

KINOPOSK_API_KEY = "4cb0d1a1-46a0-4cf2-86a3-8321e4e5fdc5"  # TODO: Bad practice


@shared_task
async def fetch_kinopoisk_rating(keyword):
    client = KPClient(KINOPOSK_API_KEY)

    production = await client.search_movie(keyword)

    return production[0].raiting.kinopoisk.value


@shared_task
async def fetch_seasons(show_name):
    client = KPClient(KINOPOSK_API_KEY)

    show = await client.search_movie(show_name)
    seasons = await client.get_seasons_data(show[0].id.kinopoisk)

    return seasons


@shared_task
async def fetch_episodes(show_name, season_number):
    seasons = await fetch_seasons(show_name)
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

    asyncio.run(fetch_episodes("Game of Thrones", 1))
