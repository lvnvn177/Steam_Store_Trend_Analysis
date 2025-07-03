import requests
import csv
import time
import json # Import json for parsing SteamSpy 'all' endpoint response

# Function to get all Steam games (from Steam Web API - not used for this request, but kept for completeness)
def get_all_steam_games():
    """
    Fetches the list of all Steam games from the Steam Web API.

    Returns:
        list: A list of dictionaries, where each dictionary represents a game
              with its "appid" and "name". Returns an empty list on failure.
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("applist", {}).get("apps", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Steam API: {e}")
        return []

def get_steam_game_details(appid):
    """
    Fetches detailed information for a given appid from the Steam Store API.

    Args:
        appid (int): The appid of the game.

    Returns:
        dict: A dictionary containing the game's details, or None on failure.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and data[str(appid)]["success"]:
            return data[str(appid)]["data"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Steam game details for appid {appid}: {e}")
    return None

def get_steamspy_game_details(appid):
    """
    Fetches detailed information for a given appid from the SteamSpy API.

    Args:
        appid (int): The appid of the game.

    Returns:
        dict: A dictionary containing the game's details, or None on failure.
    """
    url = f"http://steamspy.com/api.php?request=appdetails&appid={appid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SteamSpy game details for appid {appid}: {e}")
    return None

def get_all_steamspy_games_data():
    """
    Fetches the list of all Steam games with their details from the SteamSpy API.
    This endpoint provides 'positive' and 'negative' review counts.

    Returns:
        dict: A dictionary where keys are appids and values are game details,
              or an empty dictionary on failure.
    """
    url = "http://steamspy.com/api.php?request=all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all games data from SteamSpy API: {e}")
        return {}

def save_games_to_csv(games, filename):
    """
    Saves a list of games to a CSV file.

    Args:
        games (list): A list of game dictionaries to save.
        filename (str): The name of the output CSV file.
    """
    if not games:
        print(f"No games to save to {filename}.")
        return

    # Dynamically determine fieldnames from the first game's keys
    # Ensure 'appid' and 'name' are always first if present
    all_keys = set()
    for game in games:
        all_keys.update(game.keys())
    fieldnames = sorted(list(all_keys))
    if "appid" in fieldnames:
        fieldnames.remove("appid")
        fieldnames.insert(0, "appid")
    if "name" in fieldnames:
        fieldnames.remove("name")
        fieldnames.insert(1, "name")


    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(games)
        print(f"Successfully saved {len(games)} games to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file {filename}: {e}")

def process_and_save_game_details(games_to_process, filename="steam_games_processed.csv"):
    """
    Processes a list of games, fetches details from Steam and SteamSpy APIs,
    and saves the combined data to a CSV file.

    Args:
        games_to_process (list): A list of game dictionaries (at least with 'appid' and 'name') to process.
        filename (str): The name of the output CSV file.
    """
    if not games_to_process:
        print("No games to process for detailed information.")
        return

    # Define all possible fieldnames to ensure consistent CSV headers
    # This list should cover all fields you expect from both APIs
    fieldnames = [
        "appid", "name", "is_free", "detailed_description", "about_the_game",
        "short_description", "header_image", "website", "pc_requirements",
        "legal_notice", "developers", "publishers", "price_overview",
        "metacritic", "categories", "genres", "screenshots", "movies",
        "release_date", "background", "positive", "negative", "score_rank", "tags"
    ]

    processed_games_data = []

    for i, game in enumerate(games_to_process):
        print(f"Processing game {i+1}/{len(games_to_process)}: {game.get('name', 'Unknown Name')} (AppID: {game['appid']})")
        appid = game["appid"]
        steam_details = get_steam_game_details(appid)
        steamspy_details = get_steamspy_game_details(appid)

        if steam_details and steamspy_details:
            combined_data = {
                "appid": appid,
                "name": steam_details.get("name"),
                "is_free": steam_details.get("is_free"),
                "detailed_description": steam_details.get("detailed_description"),
                "about_the_game": steam_details.get("about_the_game"),
                "short_description": steam_details.get("short_description"),
                "header_image": steam_details.get("header_image"),
                "website": steam_details.get("website"),
                "pc_requirements": steam_details.get("pc_requirements"),
                "legal_notice": steam_details.get("legal_notice"),
                "developers": steam_details.get("developers"),
                "publishers": steam_details.get("publishers"),
                "price_overview": steam_details.get("price_overview"),
                "metacritic": steam_details.get("metacritic"),
                "categories": steam_details.get("categories"),
                "genres": steam_details.get("genres"),
                "screenshots": steam_details.get("screenshots"),
                "movies": steam_details.get("movies"),
                "release_date": steam_details.get("release_date"),
                "background": steam_details.get("background"),
                "positive": steamspy_details.get("positive"),
                "negative": steamspy_details.get("negative"),
                "score_rank": steamspy_details.get("score_rank"),
                "tags": steamspy_details.get("tags")
            }
            processed_games_data.append(combined_data)
        else:
            print(f"Skipping game {game.get('name', 'Unknown Name')} (AppID: {appid}) due to missing details from APIs.")

        # Respect API rate limits
        time.sleep(1.5)  # 200 requests per 5 minutes for Steam API

    save_games_to_csv(processed_games_data, filename)


if __name__ == "__main__":
    # 1. Get all games data from SteamSpy API
    all_steamspy_raw_data = get_all_steamspy_games_data()

    if all_steamspy_raw_data:
        # Convert dictionary to a list of dictionaries for sorting
        games_for_sorting = []
        for appid, details in all_steamspy_raw_data.items():
            # Ensure 'positive' key exists and is an integer for sorting
            if 'positive' in details and details['positive'] is not None:
                try:
                    details['positive'] = int(details['positive'])
                except ValueError:
                    details['positive'] = 0 # Default to 0 if not a valid number
            else:
                details['positive'] = 0 # Default to 0 if missing or None

            # Add appid to the details dictionary for consistent processing
            details['appid'] = int(appid) # Ensure appid is int

            games_for_sorting.append(details)

        # Sort games by 'positive' reviews in descending order
        # Filter out games that don't have a 'name' or 'appid' before sorting
        sorted_games_by_positive = sorted(
            [game for game in games_for_sorting if 'name' in game and 'appid' in game],
            key=lambda x: x.get('positive', 0),
            reverse=True
        )

        # Select the top 500 games
        top_500_games_list = sorted_games_by_positive[:500]

        # 2. Save the top 500 game list (appid, name, positive) to a CSV
        top_500_list_filename = "data/top_500_steamspy_games_list.csv"
        # save_games_to_csv function now handles dynamic fieldnames, so it will include 'positive'
        save_games_to_csv(top_500_games_list, top_500_list_filename)

        # 3. Fetch and save detailed information for these top 500 games
        processed_details_filename = "data/steam_games_processed_top_500.csv"
        process_and_save_game_details(top_500_games_list, processed_details_filename)
    else:
        print("Failed to retrieve any SteamSpy game data for processing.")