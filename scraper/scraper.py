from bs4 import BeautifulSoup
import requests
import os
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time

driver = webdriver.Chrome()
file_num = int(0) 
df= {'Name':[],'Link':[],'Cuisine':[],'Price':[],'Address':[],'Rating':[],'Contact':[]}

query = "Gomti Nagar"
driver.get(f'https://www.zomato.com/lucknow/restaurants')
time.sleep(10)  # Allow page to load
# Scroll down to load more restaurants
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10)

# Find all restaurant elements
restaurants = driver.find_elements(By.CLASS_NAME, "sc-1mo3ldo-0")  # Update class as needed

# Extract restaurant names and links
restaurant_data = []
for i in range(len(restaurants)):
    try:
        # Refresh restaurant elements (DOM may change)
        restaurants = driver.find_elements(By.CLASS_NAME, "sc-1mo3ldo-0")  # Update class
        hotel = restaurants[i]
        
        # Extract name
        name_element = hotel.find_element(By.TAG_NAME, "h4")
        name = name_element.text
        
        # Extract link
        link_element = hotel.find_element(By.TAG_NAME, "a")
        restaurant_link = link_element.get_attribute("href")

        print(f"Extracting details for: {name}")
        print(f"Link: {restaurant_link}")

        # Click the restaurant link
        driver.execute_script("arguments[0].click();", link_element)
        time.sleep(6)  # Allow page to load

        # Extract details from the new page
        try:
            cuisine = driver.find_element(By.CLASS_NAME, "sc-gVyKpa.fXdtVd").text  # Update class for cuisine
        except:
            cuisine = "Cuisine not found"

        try:
            price = driver.find_element(By.CLASS_NAME, "sc-bEjcJn.ePRRqr").text  # Update class for price
        except:
            price = "Price not found"

        try:
            address = driver.find_element(By.CLASS_NAME, "sc-clNaTc.ckqoPM").text  # Update class for address
        except:
            address = "Address not found"

        try:
            rating = driver.find_element(By.CLASS_NAME, "sc-1q7bklc-1.cILgox").text  # Update class for rating
        except:
            rating = "Rating not found"
            
        try:
            contact = driver.find_element(By.CLASS_NAME, "sc-bFADNz.leEVAg").text  # Update class for rating
        except:
            contact = "Rating not found"

        # Store extracted data
        restaurant_data.append({
            "name": name,
            "link": restaurant_link,
            "cuisine": cuisine,
            "price": price,
            "address": address,
            "rating": rating,
            "Contact": contact
        })
        df['Name'].append(name)
        df['Link'].append(restaurant_link)
        df['Cuisine'].append(cuisine)
        df['Price'].append(price)
        df['Address'].append(address)
        df['Rating'].append(rating)
        df['Contact'].append(contact)
        
        # Print extracted details
        print(f"Name: {name}\nLink: {restaurant_link}\nCuisine: {cuisine}\nPrice: {price}\nAddress: {address}\nRating: {rating}\n{'-'*50}")

        # Go back to the main restaurant list
        driver.back()
        time.sleep(8)  # Allow list page to reload

    except Exception as e:
        print(f"Error extracting details for restaurant {i}: {e}")

# Close the driver
driver.quit()

df1=pd.DataFrame(df)
df1.to_csv('mydata.csv',index=False)

# Print all extracted data
print("\nFinal Extracted Data:")
for data in restaurant_data:
    print(data)