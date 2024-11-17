import os
import time  # Import time for adding delay
import requests
from bs4 import BeautifulSoup

# Get URL and file name from the user
url = input("Enter URL of site you want to scrape: ")
crt = input("Save in current folder as: ") + ".txt"

# Path to save the scraped data
save_path = 'scraped_data'

# Check if the directory exists, if not, create it
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"Directory '{save_path}' created.")

# Ask the user for what they're looking for (tag, class, or ID)
find = input("What are you looking for (tag/class/id, or leave blank for full page): ").lower().strip()
search_value = input("Enter the value (tag name, class name, or id, or leave blank for full page): ").strip()

# Make a request to the website
try:
    print("Fetching the URL, please wait...")
    time.sleep(2)  # Add a 2-second delay before making the request
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    exit()

# Parse the page content
soup = BeautifulSoup(response.text, 'html.parser')

# Scrape the content based on user input or get the full page
if find == '' or search_value == '':
    # Output the entire page as plain text
    elements = [soup.get_text()]
else:
    if find == 'tag':
        elements = soup.find_all(search_value)
    elif find == 'class':
        elements = soup.find_all(class_=search_value)
    elif find == 'id':
        elements = soup.find_all(id=search_value)
    else:
        print("Invalid input. Please enter 'tag', 'class', or 'id', or leave blank for full page.")
        exit()

# Add a delay before writing data to file
print("Processing the data, please wait...")
time.sleep(1)  # Add a 1-second delay before processing the data

# Write the data to a file
file_path = os.path.join(save_path, crt)
try:
    with open(file_path, 'w', encoding='utf-8') as file:
        for element in elements:
            if isinstance(element, str):  # Handle the case where the entire page text is saved
                file.write(element + '\n')
            else:
                file.write(element.get_text() + '\n')
    print(f"Data saved to '{file_path}'.")
except Exception as e:
    print(f"Error saving data: {e}")
