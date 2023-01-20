from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the search term and result count
search_term = "Betrayal"
num_per_page = 9
# num_per_page = 18
# num_per_page = 30


# add some options for the chrome instance
options = Options()
options.add_argument('--headless')      # no one likes a pop-up
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')     # probably unnecessary but should handle potential mem issues

# # Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the Steam Workshop search page
driver.get(f"https://steamcommunity.com/workshop/browse/?appid=286160&searchtext={search_term}&numperpage={num_per_page}")

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "workshopItem")))

# instantiate a dictionary containing WS item title as key and subsequent info as values
item_information = {}

# instantiate a list for subsequent links
sublinks_to_scrape = []

duplicate_name_counter = 1
id_int = 0

# Scrape the workshop page for relevant data and sublinks
items = driver.find_elements(By.CLASS_NAME, "workshopItem")
for item in items:
    title = item.find_element(By.CLASS_NAME, "workshopItemTitle").text
    dict_key = title
    author_id = item.find_element(By.CLASS_NAME, 'workshop_author_link').text
    author_id_link = item.find_element(By.CLASS_NAME, 'workshop_author_link').get_attribute("href")

    image_url = item.find_element(By.CLASS_NAME, "workshopItemPreviewImage").get_attribute("src")
    file_rating_image = item.find_element(By.CLASS_NAME, "fileRating").get_attribute("src")

    id_key = id_int
    link = item.find_element(By.CLASS_NAME, "ugc").get_attribute("href")
    sublinks_to_scrape.append((link, id_key))

    id_int += 1

    if dict_key in item_information:
        while dict_key in item_information:     # add iterating numbers to duplicate title to prevent overriding entries
            duplicate_name_counter += 1
            dict_key = title + '(' + str(duplicate_name_counter) + ')'
        item_information[dict_key] = {'title': title, 'image_url': image_url, 'file_rating_image': file_rating_image,
                                      'link': link, 'author_id': author_id, 'author_id_link': author_id_link,
                                      'id_key': id_key}

    else:
        item_information[dict_key] = {'title': title, 'image_url': image_url, 'file_rating_image': file_rating_image,
                                      'link': link, 'author_id': author_id, 'author_id_link': author_id_link,
                                      'id_key': id_key}
        duplicate_name_counter = 1


# TODO: scrape sublinks for game_category, number_of_players, play_time, etc. and update corresponding item_information
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

if __name__ == '__main__':
    # pass

    print(item_information)
    #
    # for key, values in item_information.items():
    #     print(f"{key}: {values}")
    #
