import tweepy
import var
import pandas as pd

def create_tweepy_client():
    return tweepy.Client(
        consumer_key=var.consumer_key,
        consumer_secret=var.consumer_secret,
        access_token=var.access_token,
        access_token_secret=var.access_token_secret
    )

def create_tweepy_client_v1():
    auth = tweepy.OAuthHandler(
        var.consumer_key, 
        var.consumer_secret)
    auth.set_access_token(
        var.access_token, 
        var.access_token_secret)
    
    return tweepy.API(auth)

def publish_tweet(client, tweet):
    if var.SHOULD_PUBLISH_TWEET: 
        client.create_tweet(text=tweet)

def publish_tweet_w_img(client, image_path, message):
    if var.SHOULD_PUBLISH_TWEET: 
        client_v1 = create_tweepy_client_v1()
        media = client_v1.media_upload(filename = image_path)
        media_id = media.media_id
        client.create_tweet(text = message, media_ids = [media_id])

if __name__ == "__main__":

    client = create_tweepy_client()

    df = pd.read_csv('choix_utilisateur.csv', sep=';')

    article = df.to_dict(orient='records')[0]

    tweet = article['tweet']
    img = article['Image']
    include_image = article['Ajouter image']

    print(f'---------------------------—{tweet}')
    print(f'---------------------------—{img}')
    print(f'---------------------------—{include_image}')

    if include_image == "yes":
        publish_tweet_w_img(client, img, tweet)
    elif include_image == "no":
        publish_tweet(client, tweet) 
    else:
        pass
