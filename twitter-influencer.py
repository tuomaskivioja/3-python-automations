import time
import os
import json
from requests_oauthlib import OAuth1Session


consumer_key = 'INSERT'
consumer_secret = 'INSERT'

jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "How do you comfort a JavaScript bug? You console it.",
    "Why couldn't the div escape? Because its parent had a position: relative.",
    "Why do Java developers wear glasses? Because they can't C#.",
    "What's a programmer's favorite hangout place? Foo Bar!",
    "What do you call an algorithm that feels comfortable in its own code? A well-encapsulated method.",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "What do you call a programmer from Finland? Nerdic.",
    "Why do Python programmers prefer snakes? Because they come with their own scales."
]


# Check if we already have access tokens saved
tokens_file = 'twitter_tokens.json'
if os.path.exists(tokens_file):
    with open(tokens_file, 'r') as file:
        tokens = json.load(file)
    access_token = tokens['access_token']
    access_token_secret = tokens['access_token_secret']
else:
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Save the obtained tokens to a file for future use
    with open('twitter_tokens.json', 'w') as file:
        json.dump({
            'access_token': access_token,
            'access_token_secret': access_token_secret
        }, file)


# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)


# Function to read the current index from a file
def read_index():
    try:
        with open('last_joke_index.txt', 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return -1


# Function to save the current index to a file
def save_index(index):
    with open('last_joke_index.txt', 'w') as file:
        file.write(str(index))


# Function to post a joke to Twitter
def post_joke(jokes_list):
    # Read the last posted index
    last_index = read_index()
    # Get the next joke index
    next_index = (last_index + 1) % len(jokes_list)

    # Get the joke text
    joke = jokes_list[next_index]

    # Update the OAuth session if needed (code from your OAuth setup)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    # Making the request to post the tweet
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": joke}
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    else:
        print("Tweet posted: {}".format(joke))

    # Save the index of the posted joke
    save_index(next_index)


# Main logic to run the bot
def run_bot():
    while True:
        post_joke(jokes)
        time.sleep(21600)  # 6 hours in seconds


# Execute the bot
run_bot()