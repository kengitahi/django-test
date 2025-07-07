import requests
from celery import shared_task

# from .models import Movie, Show

KINOPOSK_API_KEY = "60BF9ZA-Z1TMXKQ-QGZ6ZW3-TCH68SG"


@shared_task
def fetch_kinopoisk_rating(title):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=1&query={title}"
    headers = {
        "X-API-KEY": KINOPOSK_API_KEY,
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        movie_data = data["docs"][0]
        rating = movie_data.get("rating", {}).get("kp", None)

        if rating is None:
            rating = movie_data.get("rating", {}).get("imdb")

        return rating
    else:
        print(f"Error fetching data: {response.status_code}")


if __name__ == "__main__":
    # Example usage
    # This would typically be called from a Django view or another part of the application
    # Uncomment the line below to test the function
    fetch_kinopoisk_rating("Castlevania: Nocturne")
    pass
