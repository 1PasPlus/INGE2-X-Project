import feedparser
from datetime import datetime, timedelta
import csv

url = "https://cryptoast.fr/feed/"

try:
    feed = feedparser.parse(url)
    
    # Define the time range (e.g., the last 24 hours)
    now = datetime.now()
    time_range = timedelta(days=1)  # Adjust days, hours, minutes as needed

    # Iterate through entries and filter by the time range
    for entry in feed.entries:
        try:
            entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
            if now - entry_date <= time_range:
                print("Entry Title:", entry.title)
                print("Entry Link:", entry.link)
                print("Entry Published Date:", entry.published)
                print("Entry Summary:", entry.summary)
                print("\n")
        except Exception as e:
            print(f"Error processing entry: {e}")

    # Prepare the CSV file
    with open('rss_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'link', 'published', 'summary']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through entries and write to the CSV file
        for entry in feed.entries:
            writer.writerow({'title': entry.title, 'link': entry.link, 'published': entry.published, 'summary': entry.summary})

except Exception as e:
    print("Error:", e)
