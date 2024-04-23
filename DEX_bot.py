import tweepy
from dotenv import load_dotenv
import os
from Dex_website import *

# Function to establish API connection
def api_connection():
    try:
        # Load Environment Variables
        load_dotenv()

        bearer_token = os.getenv("bearer_token")
        api_key = os.getenv("api_key")
        api_secret_key = os.getenv("api_secret_key")
        access_token = os.getenv("access_token")
        access_token_secret = os.getenv("access_token_secret")

        # Check if environment variables are set
        if not all([bearer_token, api_key, api_secret_key, access_token, access_token_secret]):
            raise ValueError("One or more required environment variables are missing.")

        # Making API Connection
        client = tweepy.Client(bearer_token, api_key, api_secret_key, access_token, access_token_secret)
        api_auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
        api = tweepy.API(api_auth)
        
        return client, api_auth, api

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")

# Function to save API keys to .env file
def save_api_keys():
    client_id_val = input("Enter Client Key: ")
    client_secret_val = input("Enter Client Secret Key: ")
    api_key_val = input("Enter API Key: ")
    api_secret_key_val = input("Enter API Secret Key: ")
    bearer_token_val = input("Enter Bearer Key: ")
    access_token_val = input("Enter Access Token : ")
    access_token_secret_val = input("Enter Access Secret Token : ")

    # Write the API keys to the .env file
    with open(".env", "w") as f:
        f.write(f"client_id={client_id_val}\n") 
        f.write(f"client_secret={client_secret_val}\n")
        f.write(f"api_key={api_key_val}\n")
        f.write(f"api_secret_key={api_secret_key_val}\n")
        f.write(f"bearer_token={bearer_token_val}\n")
        f.write(f"access_token={access_token_val}\n")
        f.write(f"access_token_secret={access_token_secret_val}\n")

# Function to post tweets based on the day of the week


# Establish API connection
client, api_auth, api = api_connection()



# Post tweets based on the day
dex_website_post_tweet(client)


# scrap_data_from_dex_website()
