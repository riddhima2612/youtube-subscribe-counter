import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Constants
API_KEY = 'AIzaSyDjGAeCOdBhZUffT1xOeVw_Xjm1ELe8LK8'  # Replace with your YouTube Data API key
CHANNEL_ID = 'UCp-gyAGJ1Pohz7fiTvrNRKg'  # Replace with the channel ID you want to track
CSV_FILE = 'subscriber_counts.csv'

# Function to fetch subscriber count
def fetch_subscriber_count():
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        subscriber_count = data['items'][0]['statistics']['subscriberCount']
        return int(subscriber_count)
    else:
        raise ValueError("Could not retrieve data from YouTube API.")

# Function to save data to CSV
def save_data(count):
    now = datetime.now()
    new_data = pd.DataFrame({'date': [now], 'subscribers': [count]})
    
    if not os.path.isfile(CSV_FILE):
        new_data.to_csv(CSV_FILE, index=False)
    else:
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)


# Function to visualize the data
def visualize_data():
    df = pd.read_csv(CSV_FILE)
    df['date'] = pd.to_datetime(df['date'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['subscribers'], marker='o')
    plt.title('YouTube Subscriber Count Over Time')
    plt.xlabel('Date')
    plt.ylabel('Subscriber Count')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main script execution
if _name_ == "_main_":
    try:
        count = fetch_subscriber_count()
        print(f"Current subscriber count: {count}")
        save_data(count)
        visualize_data()
    except Exception as e:
        print(f"An error occurred: {e}")