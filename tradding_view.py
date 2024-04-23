from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import os
from PIL import Image
import time
import tkinter as tk
import time
import pyshorteners
from tkinter import ttk, messagebox




def scrap_all_crypto_or_stocks(stocks=True, crypto=False):
    driver = webdriver.Chrome()

    if stocks:
        stocks_url = "https://www.tradingview.com/markets/stocks-usa/market-movers-all-stocks/"
        driver.get(stocks_url)

    if crypto:
        crypto_url = "https://www.tradingview.com/markets/cryptocurrencies/prices-all/"
        driver.get(crypto_url)

    wait = WebDriverWait(driver, 30)

    while True:
        try:
            load_more_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-overflow-tooltip-text="Load More "]')))
            load_more_btn.click()
        except TimeoutException:
            print("All items loaded.")
            break

    html = driver.page_source

    driver.quit()

    stock_details = []
    soup = BeautifulSoup(html, "lxml")
    main_container = soup.find("div", class_="shadow-zuRb9wy5")
    stocks = main_container.find_all("tr", class_="listRow")

    for stock in stocks:
        stock_detail = []
        stock_name = stock.find("sup", class_="apply-common-tooltip").text
        stock_link = stock.find("a", class_="tickerName-GrtoTeat").get("href")
        stock_link = "https://www.tradingview.com" + stock_link
        stock_detail.append(stock_name)
        stock_detail.append(stock_link)
        stock_details.append(stock_detail)

    if stocks:
        # Load existing stock data from CSV if it exists
        stock_csv_path = "scrap_Data/USA Stocks.csv"
        if os.path.exists(stock_csv_path):
            existing_df = pd.read_csv(stock_csv_path)

            # Filter out rows with existing stock names
            new_data = [stock for stock in stock_details if stock[0] not in existing_df["Name"].values]

            # Append new data to the existing CSV file
            if new_data:
                new_df = pd.DataFrame(new_data, columns=["Name", "Link"])
                new_df.to_csv(stock_csv_path, mode="a", header=False, index=False)

                print("Count of Newly Added Stocks:", len(new_data))
            else:
                print("No new stocks added.")
        else:
            # If the CSV file doesn't exist, create a new one and save the scraped data to it
            df = pd.DataFrame(stock_details, columns=["Name", "Link"])
            df.to_csv(stock_csv_path, index=False)

    if crypto:
        # Load existing crypto data from CSV if it exists
        crypto_csv_path = "scrap_Data/Crypto_Currency.csv"
        if os.path.exists(crypto_csv_path):
            existing_df = pd.read_csv(crypto_csv_path)

            # Filter out rows with existing crypto names
            new_data = [crypto for crypto in stock_details if crypto[0] not in existing_df["Name"].values]

            # Append new data to the existing CSV file
            if new_data:
                new_df = pd.DataFrame(new_data, columns=["Name", "Link"])
                new_df.to_csv(crypto_csv_path, mode="a", header=False, index=False)

                print("Count of Newly Added Cryptocurrencies:", len(new_data))
            else:
                print("No new cryptocurrencies added.")
        else:
            # If the CSV file doesn't exist, create a new one and save the scraped data to it
            df = pd.DataFrame(stock_details, columns=["Name", "Link"])
            df.to_csv(crypto_csv_path, index=False)   
        

def scroll_to_y(driver, y_coord):
    # Scroll to the specified Y-coordinate using JavaScript
    driver.execute_script(f"window.scrollTo(0, {y_coord});")
    
    
# def scrap_trader_tickers():
#     post_details = []

#     usernames = ["James-Bennett","Babenski","behdark","TradingShot","KlejdiCuni","weslad"]
#     current_date = datetime.now().strftime("%b %d, %Y")
#     df_old = pd.DataFrame() 
#     try:
#         for username in usernames : 
#             driver = webdriver.Chrome()
#             wait = WebDriverWait(driver,30)
#             driver.get(f"https://www.tradingview.com/u/{username}/")
#             see_more = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"tv-button__loader")))
#             see_more = driver.find_element(by=By.CLASS_NAME,value="tv-button__loader")
#             see_more.click()

#             # Initialize variables
#             footer = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"footer")))
#             footer_location_old = footer.location["y"]
#             iterations = 0

#             # Loop until footer location stops changing or until 3 consecutive iterations
            
#             while True:
#                 # Wait for a few seconds
#                 time.sleep(2)

#                 # Get the new footer location
#                 footer = wait.until(EC.visibility_of_element_located((By.TAG_NAME,"footer")))
#                 footer_location_new = footer.location["y"]
#                 post_times = driver.find_elements(by=By.CLASS_NAME, value="tv-card-stats__time")
#                 try:
#                     timestamp = post_times[-1].get_attribute("data-timestamp")
#                     post_datetime = datetime.fromtimestamp(float(timestamp))
                
#                 except Exception as e:
#                         print(f"Error processing timestamp: {e}")
#                         continue
                    
#                 if(post_datetime.date() != current_date) : 
#                     break

#                 # Check if the footer location is not changing
#                 if footer_location_new == footer_location_old:
#                     iterations += 1
#                 else:
#                     iterations = 0  # Reset the counter if location changes

#                 # Update the old location
#                 footer_location_old = footer_location_new

#                 # Scroll to the new footer location
#                 scroll_to_y(driver, footer_location_new - 50)

#                 # Break the loop if the location has not changed after 3 consecutive iterations
#                 if iterations >= 3:
#                     break

#             html = driver.page_source
#             driver.quit()
        
#             soup = BeautifulSoup(html, "lxml")
#             trader_name_element = soup.find("h1", class_="tv-profile__name-text")
#             trader_name = trader_name_element.text if trader_name_element else None
            
#             posts_container = soup.find("div", class_="tv-card-container__columns")
#             posts = posts_container.find_all("div", class_="tv-feed__item")
            
#             for post in posts:
#                 post_detail = []
#                 post_id_element = post.get("data-widget-data")
#                 post_id = post_id_element.replace("{", "").split(",")[0].split(":")[1] if post_id_element else None
#                 post_detail.append(post_id)

#                 title_element = post.find("a", class_="tv-widget-idea__title")
#                 symbol_element = post.find("a", class_="tv-widget-idea__symbol")
#                 title = title_element.text if title_element else None
#                 symbol = symbol_element.text if symbol_element else None
#                 post_detail.append(title)
#                 post_detail.append(symbol)

#                 pred_element = post.find("span", class_="badge-PlSmolIm")
#                 pred = pred_element.text if pred_element else None
#                 post_detail.append(pred)

#                 pred_duration = post.find_all("span", class_="tv-widget-idea__timeframe")
#                 pred_duration = pred_duration[1].text if len(pred_duration) > 1 else None
#                 post_detail.append(pred_duration)

#                 post_description_element = post.find("p", class_="tv-widget-idea__description-row")
#                 post_description = post_description_element.text.strip().replace("\n", "") if post_description_element else None
#                 post_detail.append(post_description)

#                 timestamp_element = post.find('span', class_='tv-card-stats__time')
#                 if timestamp_element:
#                     if timestamp_element.get('data-timestamp'):
#                         timestamp = float(timestamp_element.get('data-timestamp'))
#                         dt_object = datetime.fromtimestamp(timestamp) if timestamp else None
#                         formatted_date = dt_object.strftime("%H:%M - %b %d, %Y") if dt_object else None
#                         formatted_date = datetime.strptime(formatted_date.split("-")[1].strip(), "%b %d, %Y")
#                     else:
#                         formatted_date = None
#                 else:
#                     formatted_date = None
#                 post_detail.append(formatted_date)
                
#                 thumbnail_src_element = post.find("source")
#                 thumbnail_src = thumbnail_src_element.get("data-src") if thumbnail_src_element else None
#                 post_detail.append(thumbnail_src)
                
#                 post_link = post.find("a", class_="tv-widget-idea__cover-link")
#                 post_link = post.find("a", class_="tv-widget-idea__cover-link").get("href") if post_link else None
#                 post_detail.append(post_link)

#                 post_detail.append(trader_name)
#                 post_detail.append("Not Posted")
                
#                 check_date = datetime.now().strftime("%Y-%m-%d")
#                 if(str(formatted_date).split(" ")[0] == str(check_date)):
#                      post_details.append(post_detail)
                
#     except requests.RequestException as e:
#         print("Request Error:", e)

#     except (AttributeError, IndexError) as e:
#         print("Attribute or Index Error:", e)

#     except Exception as e:
#         print("An unexpected error occurred:", e)
        
#     # Append new data to the CSV file if post_details is not empty
#     if(os.path.exists("scrap_Data/Trader_Scrap_Data.csv")):
#         df_old = pd.read_csv("scrap_Data/Trader_Scrap_Data.csv")
#         check_date = datetime.now().strftime("%Y-%m-%d")
#         df_old = df_old.loc[df_old["Formatted Date"] == check_date]
#         df_new = pd.DataFrame(post_details, columns=["Post Id", "Post Title", "Symbol", "Prediction", "Prediction Duration", "Post Description","Formatted Date", "Thumbnail Source", "Post Link", "Trader Name", "Status"])
#         df_combined = pd.concat([df_old, df_new], ignore_index=True)
#         df_combined.to_csv("scrap_Data/Trader_Scrap_Data.csv", header=True, index=False)
        
#     else:
#         df_new = pd.DataFrame(post_details, columns=["Post Id", "Post Title", "Symbol", "Prediction", "Prediction Duration", "Post Description","Formatted Date", "Thumbnail Source", "Post Link", "Trader Name", "Status"])
#         df_new.to_csv("scrap_Data/Trader_Scrap_Data.csv", header=True, index=False)
        
#     # Append new data to the CSV file if post_details is not empty
#     print("Count of Newly Added Data:", len(post_details))


def scrap_traders_tickers(usernames=["James-Bennett","Babenski","behdark","TradingShot","KlejdiCuni","weslad"] ):
    df_old_ids = []
    check_date = datetime.now().strftime("%Y-%m-%d")
    
    if(os.path.exists("scrap_Data/Trader_Scrap_Data.csv")):
        df_old = pd.read_csv("scrap_Data/Trader_Scrap_Data.csv")
        dates = df_old["Formatted Date"]
        df_old["Formatted Date"] = pd.to_datetime(df_old["Formatted Date"], format="%b %d, %Y")
        # Filter rows by comparing datetime objects directly
        df_old = df_old[df_old["Formatted Date"] == check_date]
        df_old_ids = df_old["Post Id"]
    usernames=["James-Bennett"]
    post_details = []
    current_date = datetime.now().strftime("%b %d, %Y")
    for username in usernames : 
                driver = webdriver.Chrome()
                wait  = WebDriverWait(driver,30)
                driver.get(f"https://www.tradingview.com/u/{username}/")
                time.sleep(10)
                
                
                see_more = driver.find_element(by=By.CLASS_NAME,value="tv-button__loader")
                see_more.click()

                footer = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))
                # footer = driver.find_element(By.TAG_NAME, "footer")
                footer_location_old = footer.location["y"]
                iterations = 0
                current_date = datetime.now()
                formatted_date = current_date.strftime("%b %d, %Y")
                while True:
                    time.sleep(2)

                    footer = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))
                    footer_location_new = footer.location["y"]
                    # post_times = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"tv-card-stats__time")))
                    # post_times = driver.find_elements(by=By.CLASS_NAME, value="tv-card-stats__time")
                    # tv-card-container__ideas
                    posts_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "tv-card-container__columns")))
                    time.sleep(5)
                    posts = posts_container.find_elements(By.CLASS_NAME,"tv-feed__item")
                    
                    
                    last_post_time = posts[-1].find_elements(By.CLASS_NAME,"tv-card-stats__time")[-1].get_attribute("title").split("-")[-1].strip()
                    
                    for post in posts:
                        post_detail = []
                        post_id_element = post.get_attribute("data-widget-data")
                        title_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__title"))
                        )
                        post_id = post_id_element.replace("{", "").split(",")[0].split(":")[1] if post_id_element else None
                        post_detail.append(post_id)
                        
                        
                        
                        title_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__title"))
                        )
                        symbol_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__symbol"))
                        )
                        title = title_element.text if title_element else None
                        symbol = symbol_element.text if symbol_element else None
                        post_detail.append(title)
                        post_detail.append(symbol)

                        # Assuming 'post' is the WebElement representing a post
                        pred_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "badge-PlSmolIm"))
                        )
                        pred = pred_element.text if pred_element else None
                        post_detail.append(pred)

                        pred_duration = post.find_elements(By.CLASS_NAME, "tv-widget-idea__timeframe")
                        pred_duration = pred_duration[1].text if len(pred_duration) > 1 else None
                        post_detail.append(pred_duration)

                        post_description_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "tv-widget-idea__description-row"))
                        )
                        post_description = post_description_element.text.strip().replace("\n", "") if post_description_element else None
                        post_detail.append(post_description)
                        
                        post_time_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "tv-card-stats__time"))
                        )
                        if(len(post.find_elements(By.CLASS_NAME,"tv-card-stats__time"))>1):
                            post_time = post.find_elements(By.CLASS_NAME,"tv-card-stats__time")[-1].get_attribute("title").split("-")[-1].strip()
                        elif(len(post.find_elements(By.CLASS_NAME,"tv-card-stats__time")) == 1):
                            post_time = post.find_element(By.CLASS_NAME,"tv-card-stats__time").get_attribute("title").split("-")[-1].strip()
                        post_detail.append(post_time)

                        # Wait for the thumbnail source element
                        thumbnail_src_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "source"))
                        )
                        thumbnail_src = thumbnail_src_element.get_attribute("data-src") if thumbnail_src_element else None
                        post_detail.append(thumbnail_src)

                        # Wait for the post link element
                        post_link_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "tv-widget-idea__cover-link"))
                        )
                        post_link = post_link_element.get_attribute("href") if post_link_element else None
                        post_detail.append(post_link)
                        
                        post_detail.append(username)
                        post_detail.append("Not Posted")
                        
                        if(str(formatted_date) == str(post_time) and (str(post_id) not in str(df_old_ids))):
                            post_details.append(post_detail)
                            

                    if(str(formatted_date) != str(last_post_time)):
                        break
                    
                        
                    if footer_location_new == footer_location_old:
                        iterations += 1
                    else:
                        iterations = 0  # Reset the counter if location changes

                    footer_location_old = footer_location_new

                    scroll_to_y(driver, footer_location_new - 50)

                    if iterations >= 3:
                        break
                    
                driver.quit()
                    
    if(os.path.exists("scrap_Data/Trader_Scrap_Data.csv")):
        df_old["Formatted Date"] = dates
        df_new = pd.DataFrame(post_details, columns=["Post Id", "Post Title", "Symbol", "Prediction", "Prediction Duration", "Post Description","Formatted Date", "Thumbnail Source", "Post Link", "Trader Name", "Status"])
        df_new = df_new[~df_new['Post Id'].isin(df_old["Post Id"])]
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        print(len(df_old))
        print(len(df_new))
        print(len(df_combined))
        df_combined.to_csv("scrap_Data/Trader_Scrap_Data.csv", header=True, index=False)
            
    else:
        df_new = pd.DataFrame(post_details, columns=["Post Id", "Post Title", "Symbol", "Prediction", "Prediction Duration", "Post Description","Formatted Date", "Thumbnail Source", "Post Link", "Trader Name", "Status"])
        df_new.to_csv("scrap_Data/Trader_Scrap_Data.csv", header=True, index=False)
        
    # Append new data to the CSV file if post_details is not empty
    print("Count of Newly Added Data:", len(post_details))    
                    

def cryptocurrencies_news_trading_view():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (necessary for headless mode)

    # Set up Selenium WebDriver with headless Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # URL of the TradingView's crypto news section
    url = 'https://www.tradingview.com/markets/cryptocurrencies/news/'
    driver.get(url)

    # Wait until the main container is present and visible
    wait = WebDriverWait(driver, 10)
    main_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'list-iTt_Zp4a')))

    # Get the page source after it has fully loaded
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(page_source, 'lxml')

    # Find all the news posts
    post_details = []
    posts = soup.find_all("a", class_="card-rY32JioV")
    for post in posts:
        post_link = post.get("href")
        post_id = post.get("data-id")
        post_meta = post.find("div", class_="header-rY32JioV")
        if post_meta:
            post_time = post_meta.find("relative-time")
            post_category = post_meta.find("span", class_="provider-TUPxzdRV").text

            # Check if post_title exists before accessing its text attribute
            post_title_element = post.find("div", class_="apply-overflow-tooltip")
            post_title = post_title_element.text if post_title_element else "Title Not Available"

            post_detail = [post_id, post_category, post_title, post_time.get('title') if post_time else "N/A", post_link]
            post_details.append(post_detail)

    # Convert post_details to DataFrame
    df = pd.DataFrame(post_details, columns=["Post ID", "Post Category", "Post Title", "Post Time", "Post Link"])

    # Check if the CSV file exists
    csv_file_path = "scrap_Data/tradingview_scrap_data.csv"
    if os.path.exists(csv_file_path):
        # Load existing data from CSV
        existing_df = pd.read_csv(csv_file_path)

        # Filter out rows with existing post IDs
        new_data = df[~df["Post ID"].isin(existing_df["Post ID"])]

        # Append new data to the existing CSV file
        new_data.to_csv(csv_file_path, mode='a', header=False, index=False)

        # Calculate and print the count of newly added data
        newly_added_count = len(new_data)
        print("Count of Newly Added Data:", newly_added_count)
    else:
        # If the CSV file doesn't exist, create a new one and save the scraped data to it
        df.to_csv(csv_file_path, index=False)

        # Print that all data is newly added since the CSV file didn't exist previously
        print("Count of Newly Added Data: All Data is Newly Added")

    print("Data appended to CSV file successfully.")
    
 
def crypto_and_stock(client,crypto=False,youtube_link = "https://youtu.be/aR9JtJ652F0",telegram="https://t.me/dexwirenews"):
    try:
        s = pyshorteners.Shortener()
        youtube_link = s.tinyurl.short(youtube_link)
        telegram = s.tinyurl.short(telegram)
        driver = webdriver.Chrome()
        # logging.basicConfig(filename='twitter_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        if(crypto):
            
            df = pd.read_csv("scrap_Data/Crypto_Currency.csv")
            stock_links = df["Link"]
        else:
            df = pd.read_csv("scrap_Data/USA Stocks.csv")
            stock_links = df["Link"]
        i=0
        for link in stock_links:
            driver.get(link)

            # Wait for all elements to be visible
            wait = WebDriverWait(driver, 30)  # Adjust the timeout as needed
            if(i==0):
                # element_to_capture = driver.find_element(by=By.CLASS_NAME,value="symbolRow-OJZRoKx6")
                user = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"tv-header__user-menu-button")))
                user.click()
                
                menu= wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "menu-krYvcygz")))
                darkmode_btn =driver.find_element(By.CLASS_NAME, "input-fwE97QDf")
                darkmode_btn.click()

                element_to_click = driver.find_element(By.TAG_NAME, "body")
                element_to_click.click()
                i+=1

            # Wait for the name element to be visible
            name_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title-HFnhSVZy")))
            name = name_element.text

            # Wait for the price element to be visible
            price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "lastContainer-JWoJqCpY")))
            price = price_element.text

            # Wait for the close time element to be visible
            close_time_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "lastUpdateTime-pAUXADuj")))
            close_time = close_time_element.text  # Assuming the format remains consistent

            # Wait for the market trend element to be visible
            market_trend_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "change-JWoJqCpY")))
            market_trend = market_trend_element.text.split(" ")[0].replace("\n", ",")  # Assuming the format remains consistent

            # Wait for the range button (5 days) to be clickable
            ranges_button_div = driver.find_element(By.CLASS_NAME, "block-sjmalUvv")

            # Find all buttons inside the parent div
            range_buttons = ranges_button_div.find_elements(By.TAG_NAME, "button")

            for button in range_buttons:
                if "5 days" in button.text:
                    range_button = button
                    range_button.click()
                    break
            
            
            
            element_to_capture = driver.find_element(by=By.CLASS_NAME,value="container-lu7Cy9jC")
            location = element_to_capture.location
            size = element_to_capture.size
            # Crop the screenshot to capture only the desired element
            x = location['x']
            y = location['y']
            width = size['width']
            height = size['height']
            element_screenshot = f"Charts_ss/{name}_chart.png"
            driver.get_screenshot_as_file(element_screenshot)
            crop_chart(element_screenshot)
                
            # Wait for the 'Take a snapshot' button to be clickable
        
            
            snapshot_button = driver.find_element(by=By.CSS_SELECTOR,value='button[title="Take a snapshot"]')
            location = snapshot_button.location
            scroll_to_y(driver, -10)
            
            # time.sleep(2)
            snapshot_button.click()

            # Wait for the snapshot popup to appear
            snapshot_popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "popup-SXJIfS25")))

            # Find the 'Copy link to the chart image' option
            copy_link_option = snapshot_popup.find_element(By.CSS_SELECTOR, 'div[data-name="copy-link-to-the-chart-image"]')

            # Click on 'Copy link to the chart image'
            copy_link_option.click()
            time.sleep(3)

            # Get the clipboard content using Tkinter
            root = tk.Tk()
            root.withdraw()
            clipboard_content = root.clipboard_get()
            
            if '−' in market_trend:
                market_trend = market_trend.replace('−','-$').replace(',-$',' (-')
                
            else:
                market_trend =  market_trend.replace("+","+$").replace(',+$',' (+')
            tag_name = name.replace(' ', '').replace("'", '')
            
            signup_link = "https://dexwirenews.com/SMS"
            
            if(crypto):
                data = pd.read_csv("scrap_Data/Crypto_Currency.csv")
                metaphor = data.loc[data["Name"]==name]["Metaphor"]
                tags = f"#TradingView #CryptoCurrency #{tag_name} {'#Declining' if '-' in market_trend else '#Rising'}"
                tweet_text = f"{name} (COIN: ${metaphor[0]}): ${price}\nPrice Action:{market_trend})\n\nSign Up for 💯% FREE Text Message Notifications 📱\n{signup_link}\n\nFollow us on Telegram >> {telegram}\n\n{tags}"
            else:
                
                data = pd.read_csv("scrap_Data/USA Stocks.csv")
                metaphor = data.loc[data["Name"]==name]["Metaphor"]
                tags = f"#TradingView #US_Stocks #{tag_name} {'#Declining' if '-' in market_trend else '#Rising'}"
                tweet_text = f"{name} (Stock ${metaphor[0]}): ${price}\nPrice Action:{market_trend})\n\nSign Up for 💯% FREE Text Message Notifications 📱\n{signup_link}\n\nFollow us on Telegram >> {telegram}\n\n{tags}"
                

            # Post the tweet
            client.create_tweet(text=tweet_text)
            print("Tweet posted Successfully")

             
    except Exception as e:
                # logging.error(f"Error: {str(e)}")
                print(f"Error:{e}")
                return "Error: Tweet not posted"  # Return a default message if tweet posting fails
    finally:
        # Quit the WebDriver to clean up resources
        driver.quit()
        

 
    
def crop_chart(image_path):

    try:
        # Open the image you want to crop
        image = Image.open(image_path)  # Update with the path to your image

        # Get the size of the image
        width, height = image.size

        # Define the crop box based on the image size and crop 50 pixels from the top
        x = 0
        y = 50
        crop_width = width
        crop_height = height - 50  # Crop 50 pixels from the top

        # Crop the image using the defined box
        cropped_image = image.crop((x, y, x + crop_width, y + crop_height))

        # Save or display the cropped image
        cropped_image.save(image_path)  # Save the cropped image to a file
    
    except Exception as e:
        print(e)
        
        
def ticker_tweet(no_of_tweets,client,trader = "all",interval = 0.5,signup_link = "https://dexwirenews.com/SMS",telegram="https://t.me/dexwirenews") :    
    
    if os.path.exists("scrap_Data/Trader_Scrap_Data.csv"):
        df = pd.read_csv("scrap_Data/Trader_Scrap_Data.csv")
        df = df[df["Trader Name"].isin(trader)]
        j=0
        for i in range(len(df)):
            data = df.iloc[i]
            i+=1
            status = data["Status"]
            if (status == "Not Posted") :
                post_id = data["Post Id"]
                trader_name = data["Trader Name"]
                date = data["Formatted Date"]
                prediction = data["Prediction"]
                post_title = data["Post Title"]
                symbol = data["Symbol"]
                duration = data["Prediction Duration"]
                post_link = data["Post Link"]
                tags = f"#{trader_name} #{symbol} #TradingVIew #{prediction}"
                # \n\nhttps://www.tradingview.com{post_link}
                tweet_text = f"{post_title}\n{date}\nPrediction: {prediction}\n{symbol}, {duration}\n\nSign Up for 💯% FREE Text Message Notifications 📱\n{signup_link}\n\nFollow us on Telegram >> {telegram}\n\n{tags}"
                try:
                    client.create_tweet(text=tweet_text)
                    df.at[i, "Status"] = "posted"
                    df.to_csv("scrap_Data/Trader_Scrap_Data.csv", index=False)  
                    print(f"{post_id} Posted Successfully")
                    j+=1
                    time.sleep(60*interval)
                except Exception as e:
                    print(e)
            if(j==no_of_tweets):
                break

            
            

        
        