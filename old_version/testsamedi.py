from gnews import GNews

client = GNews()  # Assuming you have gnews installed correctly

def get_top_news():
    articles = client.get_news()  # Fetch top news
    titles = [article["title"] for article in articles]  # Access title from dictionary
    return titles

def get_keyword_news(keyword):
    articles = client.get_news(keyword=keyword)  # Fetch news by keyword
    titles = [article["title"] for article in articles]  # Access title from dictionary
    return titles

user_choice = input("Voulez-vous des actualités Top du moment (1) ou des actualités en rapport avec un mot-clé (2) ? ")

if user_choice == '1':
    titles = get_top_news()
else:
    keyword = input("Entrez votre mot-clé : ")
    titles = get_keyword_news(keyword)

# Print or use the list of titles as needed
print("Titres des actualités :", titles)
