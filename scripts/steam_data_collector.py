import requests
import csv

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

def save_games_to_csv(games, filename="steam_games.csv"):
    """
    Saves a list of games to a CSV file.

    Args:
        games (list): A list of game dictionaries to save.
        filename (str): The name of the output CSV file.
    """
    if not games:
        print("No games to save.")
        return

    # Specify the fieldnames for the CSV header
    fieldnames = ["appid", "name"]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(games)
        print(f"Successfully saved {len(games)} games to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    all_games = get_all_steam_games()
    if all_games:
        save_games_to_csv(all_games)
