import tweepy
import var
import pandas as pd
import time

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
    type_of_content = article['type de contenu']

    print(f'---------------------------—{tweet}')
    print(f'---------------------------—{img}')
    print(f'---------------------------—{include_image}')

    if include_image == "yes":

        if type_of_content == 1:
            print("posting tweet 1 w image")
            publish_tweet_w_img(client, img, tweet)
        elif type_of_content == 2:
            print("posting tweet 2 w image")
            publish_tweet_w_img(client, img, tweet)
        elif type_of_content == 3:
            print("posting tweet 3 w image")
            publish_tweet_w_img(client, img, tweet)

        elif type_of_content == 4:

            # Diviser la chaîne en utilisant ":" comme délimiteur
            tweets_list = tweet.split('Tweet ')[1:]
            for i in range (0,len(tweets_list)):

                separate_tweet = tweets_list[i].strip()
                final_tweet_list = separate_tweet.split(':')[1:]
                final_tweet = final_tweet_list[0]
                publish_tweet_w_img(client, img, final_tweet)
                print("posting tweet 4 w image")
                time.sleep(2)
   

    elif include_image == "no":
        
        if type_of_content == 1:
            publish_tweet(client, tweet)
            print("posting tweet 1 without image")
        elif type_of_content == 2:
            publish_tweet(client, tweet)
            print("posting tweet 2 without image")
        elif type_of_content == 3:
            publish_tweet(client, tweet)
            print("posting tweet 3 without image")

        elif type_of_content == 4:

            # Diviser la chaîne en utilisant ":" comme délimiteur
            tweets_list = tweet.split('Tweet ')[1:]
            for i in range (0,len(tweets_list)):

                separate_tweet = tweets_list[i].strip()
                final_tweet_list = separate_tweet.split(': ')[1:]
                final_tweet = final_tweet_list[0]
                publish_tweet(client, final_tweet)
                print("posting tweet 4 without image")
                time.sleep(2)

    else:
        print("Error no image")
        pass
                
