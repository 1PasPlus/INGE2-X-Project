import pandas as pd
from gnews import NewsClient

def get_and_save_news(keyword, number_of_articles, output_filename="news.csv"):
  """
  Fetches news articles from Google News based on a keyword, 
  saves them to a CSV file, and returns the number of articles found.

  Args:
      keyword (str): The keyword to search for in news articles.
      number_of_articles (int): The maximum number of articles to retrieve.
      output_filename (str, optional): The filename for the CSV file. 
          Defaults to "news.csv".

  Returns:
      int: The number of articles retrieved and saved to the CSV file.
  """

  # Define language (optional)
  lang = "en"  # Change this to your preferred language (e.g., "fr" for French)

  client = NewsClient(lang=lang)
  articles = client.get_news(keyword, max_results=number_of_articles)

  # Create pandas DataFrame
  df = pd.DataFrame({
      "Title": [article.title for article in articles],
      "Link": [article.url for article in articles],
      "Date": [article.publish_date for article in articles],
      "Source": [article.source for article in articles],
      "Summary": [article.summary for article in articles]
  })

  # Save DataFrame to CSV
  df.to_csv(output_filename, index=False)

  # Return the number of articles
  return len(articles)

# Example usage (replace with your desired keyword and number of articles)
keyword = "artificial intelligence"
number_of_articles = 50
num_articles_fetched = get_and_save_news(keyword, number_of_articles)

print(f"Successfully retrieved and saved {num_articles_fetched} news articles to {output_filename}")
