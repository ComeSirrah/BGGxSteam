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
# options.add_argument('--headless')      # no one likes a pop-up TODO: BUG! STEAM WILL NOT RETURN TAGS WHILE HEADLESS
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

    id_int += 1

    if dict_key in item_information:
        while dict_key in item_information:     # add iterating numbers to duplicate title to prevent overriding entries
            duplicate_name_counter += 1
            dict_key = title + '(' + str(duplicate_name_counter) + ')'
        item_information[dict_key] = {'title': title, 'image_url': image_url, 'file_rating_image': file_rating_image,
                                      'link': link, 'author_id': author_id, 'author_id_link': author_id_link}
        sublinks_to_scrape.append((link, dict_key))

    else:
        item_information[dict_key] = {'title': title, 'image_url': image_url, 'file_rating_image': file_rating_image,
                                      'link': link, 'author_id': author_id, 'author_id_link': author_id_link}
        sublinks_to_scrape.append((link, dict_key))
        duplicate_name_counter = 1




# scrape each
# type = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# complexity = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# game_category = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# number_of_players = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# play_time = item.find_element(By.CLASS_NAME, "workshopItemTag").text
# language = item.find_element(By.CLASS_NAME, "workshopItemTag").text

# print(title, game_category, number_of_players, play_time, language, image_url)
# print([title, image_url, file_rating_image])


for sub_link in sublinks_to_scrape:
    driver.get(sub_link[0]) # taking the actual sublink and passing to driver
    wait = WebDriverWait(driver, 10)
    elements = driver.find_elements(By.CLASS_NAME, 'workshopTagsTitle')
    temp_dict = {}
    for element in elements:
        tag_value = element.find_element(By.XPATH, './following-sibling::*')
        temp_dict[element.text.rstrip(": ")] = tag_value.text # getting rid of trailing text from keys
        # print(element.text, tag_value.text)
    item_information[sub_link[1]].update(temp_dict)
    if 'Tags' in item_information[sub_link[1]]:     # remove unwanted/ problematic information
        del item_information[sub_link[1]]['Tags']
    if 'Assets' in item_information[sub_link[1]]:  # remove unwanted/ problematic information
        del item_information[sub_link[1]]['Assets']
    if 'Game Category' in item_information[sub_link[1]]:  # remove unwanted/ problematic information
        del item_information[sub_link[1]]['Game Category']

# Close the browser window
driver.quit()

if __name__ == '__main__':
    # pass
    for key, value in item_information.items():
        print(f'{key}:')
        for subkey, sub_value in value.items():
            print(f'\t\t{subkey}:\t{sub_value}')