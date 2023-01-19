from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the search term
search_term = "risk"

# add some options for the chrome instance
options = Options()
options.add_argument('--headless')      # no one likes a pop-up
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')     # probably unnecessary but should handle potential mem issues

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the Steam Workshop search page
driver.get(f"https://steamcommunity.com/workshop/browse/?appid=286160&searchtext={search_term}")

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "workshopItem")))

# instantiate a dictionary containing WS item title as key and subsequent info as values
item_information = {}

# instantiate a list for subsequent links
sublinks_to_scrape = []

duplicate_name_counter = 2

# Scrape the workshop page for relevant data and sublinks
items = driver.find_elements(By.CLASS_NAME, "workshopItem")
for item in items:
    title = item.find_element(By.CLASS_NAME, "workshopItemTitle").text
    image_url = item.find_element(By.CLASS_NAME, "workshopItemPreviewImage").get_attribute("src")
    file_rating_image = item.find_element(By.CLASS_NAME, "fileRating").get_attribute("src")
    link = item.find_element(By.CLASS_NAME, "ugc").get_attribute("href")
    sublinks_to_scrape.append(link)
    if title in item_information:
        item_information[title+'('+str(duplicate_name_counter)+')'] = title, image_url, file_rating_image, link
        duplicate_name_counter += 1
    else:
        item_information[title] = title, image_url, file_rating_image, link
        duplicate_name_counter = 2

# TODO: Create id_key value
#  add id_key value to item_information and sublinks_to_scrape to correlate data
#  scrape sublinks for game_category, number_of_players, play_time, etc. and update corresponding item_information
#  keys with values

# scrape each
# type = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# complexity = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# game_category = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# number_of_players = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# play_time = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# language = item.find_element(By.CLASS_NAME, "workshopItemTag").text

# print(title, game_category, number_of_players, play_time, language, image_url)
# print([title, image_url, file_rating_image])


# Close the browser window
driver.quit()
