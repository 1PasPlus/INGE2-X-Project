import tweepy
import var



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

choix = input("Voulez vous poster le tweet ? (1) photo (2) pas photo : ")

client = create_tweepy_client()

if choix == "1":
    img = r'INGE2-X-Project/Nature.jpeg' #CHANGEER la photo et faire avec os.path
    tweet = 'salut' # CHANGER pour que ça soit le bon tweet 
    publish_tweet_w_img(client, img, tweet)
elif choix == "2":
    tweet = "Hello, World!" # CHANGER pour que ça soit le bon tweet 
    publish_tweet(client, tweet) 
else:
    print("Choix invalide. Veuillez choisir 1 ou 2.")


if client is not None:
    print("Tweet created successfully!")
else:
    print("Error creating tweet.")
