import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv
import tweepy
from tradding_view import scrap_traders_tickers,ticker_tweet

# usernames = ["James-Bennett","Babenski","behdark","TradingShot","KlejdiCuni","weslad"]

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

def get_selected_traders():
    selected = []
    if trader1_var.get():
        selected.append("James-Bennett")
    if trader2_var.get():
        selected.append("Babenski")
    if trader3_var.get():
        selected.append("behdark")
    if trader4_var.get():
        selected.append("TradingShot")
    if trader5_var.get():
        selected.append("KlejdiCuni")
    if trader6_var.get():
        selected.append("weslad")
    
    # Add more traders as needed
    return selected

def start_scraping():
    selected_traders = get_selected_traders()
    if username_entry.get():
        selected_traders.append(username_entry.get())
    try:
        scrap_traders_tickers(selected_traders)
        messagebox.showinfo("Successful","Data Scraped")
    except:
        messagebox.showerror("Error",e)
    # print("Selected Traders:", selected_traders)
    
def save_api_keys():
    client_id_val = client_key_entry.get()
    client_secret_val = client_secret_key_entry.get()
    api_key_val = api_key_entry.get()
    api_secret_key_val = api_secret_key_entry.get()
    bearer_token_val = bearer_key_entry.get()
    access_token_val = access_key_entry.get()
    access_token_secret_val = access_secret_key_entry.get()
    
    # Clear the entry fields
    client_key_entry.delete(0, tk.END)
    client_secret_key_entry.delete(0, tk.END)
    api_key_entry.delete(0, tk.END)
    api_secret_key_entry.delete(0, tk.END)
    bearer_key_entry.delete(0, tk.END)
    access_key_entry.delete(0, tk.END)
    access_secret_key_entry.delete(0, tk.END)
    
    # Write the API keys to the .env file
    with open(".env", "w") as f:
        f.write(f"client_id={client_id_val}\n") 
        f.write(f"client_secret={client_secret_val}\n")
        f.write(f"api_key={api_key_val}\n")
        f.write(f"api_secret_key={api_secret_key_val}\n")
        f.write(f"bearer_token={bearer_token_val}\n")
        f.write(f"access_token={access_token_val}\n")
        f.write(f"access_token_secret={access_token_secret_val}\n")
        
    messagebox.showinfo("Success", "API keys saved successfully!")

# # Function to post tweets of selected traders
def post_trader_tweets():
    selected = []
    if trader1_var.get():
        selected.append("James-Bennett")
    if trader2_var.get():
        selected.append("Babenski")
    if trader3_var.get():
        selected.append("behdark")
    if trader4_var.get():
        selected.append("TradingShot")
    if trader5_var.get():
        selected.append("KlejdiCuni")
    if trader6_var.get():
        selected.append("weslad")
    if (num_tweets_entry.get()):
        num_tweets = int(num_tweets_entry.get())
    if (num_tweets > 0):
        try:
            ticker_tweet(no_of_tweets=num_tweets,client=client,trader=selected)
            messagebox.showinfo("Successful","Tweets Posted Successfully")
        except Exception as e:
            messagebox.showerror("Error",e)
    

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
api_key = os.getenv("api_key")
api_secret_key = os.getenv("api_secret_key")
bearer_token = os.getenv("bearer_token")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")


root = tk.Tk()
root.title("Twitter Bot GUI")

client, api_auth, api = api_connection()


tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

api_keys_tab = ttk.Frame(tab_control)
tab_control.add(api_keys_tab, text='API Keys')

# Add input fields for API keys
client_key_label = ttk.Label(api_keys_tab, text='Client ID:')
client_key_entry = ttk.Entry(api_keys_tab)
if(client_id):
    client_key_entry.insert(0,client_id)
client_secret_key_label = ttk.Label(api_keys_tab, text='Client Secret ID:')
client_secret_key_entry = ttk.Entry(api_keys_tab)
if(client_secret):
    client_secret_key_entry.insert(0,client_secret)
api_key_label = ttk.Label(api_keys_tab, text='API Key:')
api_key_entry = ttk.Entry(api_keys_tab)
if(api_key):
    api_key_entry.insert(0,api_key)
api_secret_key_label = ttk.Label(api_keys_tab, text='API Secret Key:')
api_secret_key_entry = ttk.Entry(api_keys_tab)
if(api_secret_key):
    api_secret_key_entry.insert(0,api_secret_key)
bearer_key_label = ttk.Label(api_keys_tab, text='Bearer Key:')
bearer_key_entry = ttk.Entry(api_keys_tab)
if(bearer_token):
    bearer_key_entry.insert(0,bearer_token)
access_key_label = ttk.Label(api_keys_tab, text='Access Key:')
access_key_entry = ttk.Entry(api_keys_tab)
if(access_token):
    access_key_entry.insert(0,access_token)
access_secret_key_label = ttk.Label(api_keys_tab, text='Access Secret Key:')
access_secret_key_entry = ttk.Entry(api_keys_tab)
if(access_token_secret):
    access_secret_key_entry.insert(0,access_token_secret)
# Add more labels and entries for other API keys
save_button = ttk.Button(api_keys_tab, text='Save', command=save_api_keys)

scraping_tab = ttk.Frame(tab_control)
tab_control.add(scraping_tab, text='Scraping')

# Add checkboxes for selecting traders
trader1_var = tk.BooleanVar()
trader2_var = tk.BooleanVar()
trader3_var = tk.BooleanVar()
trader4_var = tk.BooleanVar()
trader5_var = tk.BooleanVar()
trader6_var = tk.BooleanVar()



trader_selection_label = ttk.Label(scraping_tab, text='Select Traders:')
trader1_checkbox = ttk.Checkbutton(scraping_tab, text='James-Bennett',variable=trader1_var)
trader2_checkbox = ttk.Checkbutton(scraping_tab, text='Babenski',variable=trader2_var)
trader3_checkbox = ttk.Checkbutton(scraping_tab, text='behdark',variable=trader3_var)
trader4_checkbox = ttk.Checkbutton(scraping_tab, text='TradingShot',variable=trader4_var)
trader5_checkbox = ttk.Checkbutton(scraping_tab, text='KlejdiCuni',variable=trader5_var)
trader6_checkbox = ttk.Checkbutton(scraping_tab, text='weslad',variable=trader6_var)

# Add more checkboxes as needed

# Add input field for entering username
username_label = ttk.Label(scraping_tab, text='Enter Username:')
username_entry = ttk.Entry(scraping_tab)

start_button = ttk.Button(scraping_tab, text='Start Scraping', command=start_scraping)

# Grid or pack widgets in the API keys tab
client_key_label.grid(row=0, column=0, padx=5, pady=5)
client_key_entry.grid(row=0, column=1, padx=5, pady=5)
client_secret_key_label.grid(row=1, column=0, padx=5, pady=5)
client_secret_key_entry.grid(row=1, column=1, padx=5, pady=5)
api_key_label.grid(row=2, column=0, padx=5, pady=5)
api_key_entry.grid(row=2, column=1, padx=5, pady=5)
api_secret_key_label.grid(row=3, column=0, padx=5, pady=5)
api_secret_key_entry.grid(row=3, column=1, padx=5, pady=5)
bearer_key_label.grid(row=4, column=0, padx=5, pady=5)
bearer_key_entry.grid(row=4, column=1, padx=5, pady=5)
access_key_label.grid(row=5, column=0, padx=5, pady=5)
access_key_entry.grid(row=5, column=1, padx=5, pady=5)
access_secret_key_label.grid(row=6, column=0, padx=5, pady=5)
access_secret_key_entry.grid(row=6, column=1, padx=5, pady=5)

save_button.grid(row=7, column=1, padx=5, pady=5)



# Grid or pack widgets in the scraping tab
trader_selection_label.grid(row=0, column=0, padx=5, pady=5)
trader1_checkbox.grid(row=1, column=0, padx=5, pady=5)
trader2_checkbox.grid(row=1, column=1, padx=5, pady=5)
trader3_checkbox.grid(row=1, column=2, padx=5, pady=5)
trader4_checkbox.grid(row=2, column=0, padx=5, pady=5)
trader5_checkbox.grid(row=2, column=1, padx=5, pady=5)
trader6_checkbox.grid(row=2, column=2, padx=5, pady=5)
username_label.grid(row=3, column=0, padx=5, pady=5)
username_entry.grid(row=3, column=1, padx=5, pady=5)

start_button.grid(row=4, column=1, padx=5, pady=5)

trader_tweet_tab = ttk.Frame(tab_control)
tab_control.add(trader_tweet_tab, text='Trader Tweet')

ttk.Label(trader_tweet_tab, text='Number of Tweets:').grid(row=0,column=0)
num_tweets_entry = ttk.Entry(trader_tweet_tab)
num_tweets_entry.insert(0,1)
num_tweets_entry.grid(row=0,column=1)

trader_selection_label = ttk.Label(trader_tweet_tab, text='Select Trader:')
trader_var = tk.StringVar()

# Create radio buttons for each trader
trader1_radio = ttk.Radiobutton(trader_tweet_tab, text='James-Bennett', variable=trader_var, value='James-Bennett')
trader2_radio = ttk.Radiobutton(trader_tweet_tab, text='Babenski', variable=trader_var, value='Babenski')
trader3_radio = ttk.Radiobutton(trader_tweet_tab, text='behdark', variable=trader_var, value='behdark')
trader4_radio = ttk.Radiobutton(trader_tweet_tab, text='TradingShot', variable=trader_var, value='TradingShot')
trader5_radio = ttk.Radiobutton(trader_tweet_tab, text='KlejdiCuni', variable=trader_var, value='KlejdiCuni')
trader6_radio = ttk.Radiobutton(trader_tweet_tab, text='weslad', variable=trader_var, value='weslad')

# Set default value for the radio button
trader_var.set('James-Bennett')

# Grid the widgets
trader_selection_label.grid(row=1, column=0, padx=5, pady=5)
trader1_radio.grid(row=2, column=0, padx=5, pady=5)
trader2_radio.grid(row=2, column=1, padx=5, pady=5)
trader3_radio.grid(row=2, column=2, padx=5, pady=5)
trader4_radio.grid(row=3, column=0, padx=5, pady=5)
trader5_radio.grid(row=3, column=1, padx=5, pady=5)
trader6_radio.grid(row=3, column=2, padx=5, pady=5)

post_tweet = ttk.Button(trader_tweet_tab, text='Post Tweets', command=post_trader_tweets)

post_tweet.grid(row=4, column=1, padx=5, pady=5)
root.mainloop()




