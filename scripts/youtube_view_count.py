import requests
import csv
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

# Check if API key is available
if not api_key:
    print("Error: YOUTUBE_API_KEY not found in .env file. Please set it in your .env file.")
    exit()

try:
    youtube = build('youtube', 'v3', developerKey=api_key)
except Exception as e:
    print(f"Error building YouTube service: {e}")
    exit()

def get_youtube_review_details(game_name):
    """
    Searches for YouTube review videos for a given game and fetches their details.

    Args:
        game_name (str): The name of the game to search for.

    Returns:
        list: A list of dictionaries, where each dictionary contains details
              (Video ID, Title, Published At, Views, Likes, Comments) for each video.
              Returns an empty list on failure or no videos found.
    """
    video_details_list = []
    try:
        # Step 1: Search for videos
        search_response = youtube.search().list(
            q=f"{game_name} review",
            part="id",
            maxResults=10, # Get top 10 videos
            type="video"
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response.get('items', []) if 'videoId' in item['id']]

        if not video_ids:
            # print(f"No review videos found for '{game_name}'.")
            return []

        # Step 2: Get statistics and snippet details for the found videos
        # Requesting 'snippet' for title and publishedAt, 'statistics' for views, likes, comments
        stats_response = youtube.videos().list(
            id=",".join(video_ids),
            part="snippet,statistics"
        ).execute()

        for item in stats_response.get('items', []):
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})

            detail = {
                'Video ID': item['id'], # This is the video ID string
                'Video Title': snippet.get('title'),
                'Published At': snippet.get('publishedAt'),
                'Views': int(statistics.get('viewCount', 0)),
                'Likes': int(statistics.get('likeCount', 0)),
                'Comments': int(statistics.get('commentCount', 0))
                # Note: YouTube API no longer directly provides dislikeCount
            }
            video_details_list.append(detail)

    except Exception as e:
        print(f"Error fetching YouTube details for '{game_name}': {e}")
    return video_details_list

def save_data_to_csv(data, filename, fieldnames):
    """
    Saves a list of dictionaries to a CSV file.

    Args:
        data (list): A list of dictionaries to save.
        filename (str): The name of the output CSV file.
        fieldnames (list): A list of strings specifying the CSV header order.
    """
    if not data:
        print(f"No data to save to {filename}.")
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully saved {len(data)} entries to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file {filename}: {e}")


if __name__ == "__main__":
    input_games_list_path = "/Users/iyeongho/Desktop/Project/Data/Steam/Steam_Store_Trend_Analysis/data/top_500_steamspy_games_list.csv"
    output_youtube_data_path = "/Users/iyeongho/Desktop/Project/Data/Steam/Steam_Store_Trend_Analysis/data/youtube_review_data.csv"

    # Ensure the input file exists
    if not os.path.exists(input_games_list_path):
        print(f"Error: Input file not found at {input_games_list_path}")
        exit()

    try:
        df_games = pd.read_csv(input_games_list_path)
    except Exception as e:
        print(f"Error reading input CSV file: {e}")
        exit()

    all_youtube_video_data = []
    # Define the fieldnames for the output CSV, including 'Game Name'
    output_fieldnames = ['Game Name', 'Video Title', 'Video ID', 'Published At', 'Views', 'Likes', 'Comments']

    print(f"Starting YouTube review data collection for {len(df_games)} games...")

    for index, row in df_games.iterrows():
        game_name = row['name']
        print(f"Fetching YouTube review data for game: {game_name}")
        
        youtube_videos = get_youtube_review_details(game_name)
        
        for video in youtube_videos:
            # Add the game name to each video entry before appending
            video['Game Name'] = game_name 
            all_youtube_video_data.append(video)
        
        # Add a delay to respect YouTube API quota limits
        time.sleep(0.5) 

    # Save all collected data to a single CSV file
    save_data_to_csv(all_youtube_video_data, output_youtube_data_path, output_fieldnames)

    print("YouTube review data collection complete.")
