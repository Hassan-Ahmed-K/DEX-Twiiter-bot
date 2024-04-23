
import pandas as pd
import time
from datetime import datetime
import pyshorteners
from bs4 import BeautifulSoup
import requests
import os


def dex_website_post_tweet(client):
    try:
        s = pyshorteners.Shortener()
        
        # Load data from CSV file
        signup_link = "https://dexwirenews.com/SMS"
        
        
        df = pd.read_csv("website_scrap_data.csv")

        # Get the current day of the week (0 = Monday, 6 = Sunday)
        current_day = datetime.today().weekday()

        # Define the number of tweets to post based on the day
        if current_day in range(0, 5):  # Monday to Friday
            tweets_to_post = 4  # Adjust this number as needed
        else:  # Saturday and Sunday
            tweets_to_post = 1  # Adjust this number as needed

        # Iterate over each row in the DataFrame
        j = 0
        for i in range(tweets_to_post):
            data = df.iloc[j]
            while data["status"] == "posted":
                j += 1
                data = df.iloc[j]          
            post_id = data["Post ID"]
            heading = data["Heading"]
            description = data["Description"]
            tags = data["Categories"].strip("[]").replace(" ", "").replace("-", "").replace("'", "").split(
                ",")  # Clean up tags
            tags.append(data["Author"].replace(" ", ""))
            post_link = data["Post Link"]
            post_img = data["Thumbnail Src"]
            
            post_link = s.tinyurl.short(post_link)

            # Construct the tweet text
            tags_str = " ".join(f"#{tag.strip()}" for tag in tags)  # Format tags with #
            tweet_text = f"{heading}\n\nSign Up for 💯% FREE Text Message Notifications 📱\n{signup_link}\n\n{post_link}\n\n{tags_str}"
            # print(tweet_text)

            # Check if tweet text length is greater than 280 characters
            if len(tweet_text) > 280:
                # Remove the last tag
                tags_str = " ".join(f"#{tag.strip()}" for tag in tags[:-1])  # Exclude the last tag
                tweet_text = f"{heading}\n\nSign Up for 💯% FREE Text Message Notifications 📱\n{signup_link}\n\n{post_link}\n\n{tags_str}"

            client.create_tweet(text=tweet_text)
            df.at[j, "status"] = "posted"
            print(f"{post_id}  posted successfully!")
            j += 1
            if i != len(df) - 1:
                time.sleep(30)

    except Exception as e:
        print(f"Error posting tweet: {e}")
        
    df.to_csv("website_scrap_data.csv", index=False)
    
    
    

def scrap_data_from_dex_website():
    post_details = []
    input_date_str = input("Enter the date in the format 'Month Day, Year' (e.g., 'April 12, 2024'): ")
    date_list = []

    try:
        print("Please enter the date to retrieve posts until that date OR leave It blanks for all posts")
        input_date= input("Enter the date in the format 'Month Day, Year' (e.g., 'April 12, 2024'): ")
        
        if(input_date != ""):
            input_date = datetime.datetime.strptime(input_date, "%B %d, %Y")

            # Get the current date
            current_date = datetime.datetime.now()

            # Generate a list of dates from the input date to the current date
            date_list = []
            delta = datetime.timedelta(days=1)
            while input_date <= current_date:
                date_list.append(input_date.strftime("%B %d, %Y"))
                input_date += delta

            print(date_list)
        else:
            date_list = "all"

    except Exception as e:
        print(e)

    # Load existing data from CSV file if it exists
    if os.path.isfile("scrap_Data/website_scrap_data.csv"):
        existing_data = pd.read_csv("scrap_Data/website_scrap_data.csv")
        existing_ids = existing_data["Post ID"].tolist()
    else:
        existing_ids = []

    connection = requests.get("https://dexwirenews.com/").text
    soup = BeautifulSoup(connection, "lxml")
    total_pages = soup.find_all("a", class_="page-numbers")[-2].text

    connect = True
    i = 2
    failed_connections = []

    iteration = 0

    while i <= int(total_pages):
        if connect:
            main_div = soup.find("div", class_="theme-archive-layout")
            posts = main_div.find_all("article", class_="post")

            for post in posts:
                post_id = post.get("id")
                meta_data = post.find("ul", class_="entry-meta")
                if meta_data:
                    post_date = meta_data.find("li", class_="post-date").text.strip()
                    print(post_date)
                    if ((post_id not in existing_ids) and (post_date in date_list) or (post_id not in existing_ids) and (date_list == "all")):
                        iteration = 0
                        post_link = post.find("a", class_="post-thumbnail").get("href")
                        thumbnail_img = post.find("img", class_="attachment-post-thumbnail")
                        if thumbnail_img:
                            thumbnail_src = thumbnail_img.get("src")
                        else:
                            thumbnail_src = None
                        categories = post.find("ul", class_="post-categories")
                        if categories:
                            category_items = categories.find_all("li")
                            categories_list = [category.text for category in category_items]
                        else:
                            categories_list = []
                        heading = post.find("h2", class_="entry-title").text.strip()
                        post_author = meta_data.find("li", class_="post-author").text.strip()
                        post_comment = meta_data.find("li", class_="post-comment").text.strip()
                        post_content = post.find("div", class_="post-content")
                        if post_content:
                            post_description = post_content.find("p").text.strip()
                        else:
                            post_description = ""
                        post_detail = [post_id, categories_list, post_date, heading, post_description, post_comment,
                                    post_author, thumbnail_src, post_link, "not posted"]
                        post_details.append(post_detail)
                    if (post_date != current_date) and (current_date != "all"):
                        iteration += 1
                    if (iteration >= 3):
                        break
            if (iteration >= 3):
                break

            print(len(post_details))
            print(f"Page {i - 1} Completed")

            try:
                connection = requests.get(f"https://dexwirenews.com/page/{i}/").text
                soup = BeautifulSoup(connection, "lxml")
                i += 1
            except Exception as e:
                print(f"Connection Failed With Page {i} ")
                connect = False
                failed_connections.append(i)
                i += 1
                continue
        else:
            connect = True

    if len(failed_connections) != 0:
        retry = input("You want to retry failed Connection T or F: ")
        if retry.lower() == "t":
            failed = []
            for i in failed_connections:
                try:
                    connection = requests.get(f"https://dexwirenews.com/page/{i}/").text
                    soup = BeautifulSoup(connection, "lxml")
                except Exception as e:
                    print(f"Connection Failed With Page {i} ")
                    failed.append(i)

                main_div = soup.find("div", class_="theme-archive-layout")
                posts = main_div.find_all("article", class_="post")

                for post in posts:
                    post_id = post.get("id")
                    meta_data = post.find("ul", class_="entry-meta")
                    if meta_data:
                        post_date = meta_data.find("li", class_="post-date").text.strip()
                        if (post_id not in existing_ids) and (post_date == current_date):
                            post_link = post.find("a", class_="post-thumbnail").get("href")
                            thumbnail_img = post.find("img", class_="attachment-post-thumbnail")
                            if thumbnail_img:
                                thumbnail_src = thumbnail_img.get("src")
                            else:
                                thumbnail_src = None
                            categories = post.find("ul", class_="post-categories")
                            if categories:
                                category_items = categories.find_all("li")
                                categories_list = [category.text for category in category_items]
                            else:
                                categories_list = []
                            heading = post.find("h2", class_="entry-title").text.strip()
                            post_author = meta_data.find("li", class_="post-author").text.strip()
                            post_comment = meta_data.find("li", class_="post-comment").text.strip()
                            post_content = post.find("div", class_="post-content")
                            if post_content:
                                post_description = post_content.find("p").text.strip()
                            else:
                                post_description = ""
                            post_detail = [post_id, categories_list, post_date, heading, post_description, post_comment,
                                        post_author, thumbnail_src, post_link, "not posted"]
                            post_details.append(post_detail)

                print(f"Page {i - 1} Completed")
            print(failed)

    # Concatenate existing data with new data
    df_old = pd.read_csv("website_scrap_data.csv")
    if (current_date != "all"):
        filter_data = df_old[df_old["Date"].isin(date_list)]
        
    df_new = pd.DataFrame(post_details, columns=["Post ID", "Categories", "Date", "Heading", "Description",
                                                "Comment", "Author", "Thumbnail Src", "Post Link", "status"])
    df_combined = pd.concat([filter_data, df_new], ignore_index=True)

    # Save the combined DataFrame to CSV
    df_combined.to_csv("scrap_Data/website_scrap_data.csv", index=False)




