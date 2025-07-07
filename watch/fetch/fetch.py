import json
import os

import requests

movies_json_url = "https://channelsapi.s3.amazonaws.com/media/test/movies.json"
shows_json_url = "https://channelsapi.s3.amazonaws.com/media/test/shows.json"

SAVE_DIR = "./watch/fetched_data"


def fetch_json_data(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        movies_data = response.json()

        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        save_file_path = os.path.join(SAVE_DIR, f"{filename}.json")

        with open(save_file_path, "w") as movies_file:
            json.dump(movies_data, movies_file, indent=4)

        print(f"Successfully dumped JSON from '{url}' to '{filename}.json'")
    except requests.RequestException as e:
        print(f"Error fetching movies or shows data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from response: {e}")
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")


if __name__ == "__main__":
    fetch_json_data(movies_json_url, "movies")
    fetch_json_data(shows_json_url, "shows")
