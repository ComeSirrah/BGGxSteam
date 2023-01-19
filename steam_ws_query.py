import requests


class SteamWorkshop:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_app_id(self, game_name='Tabletop Simulator'):
        url = f'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response = requests.get(url)
        data = response.json()

        if game_name:
            steam_app_id = [app['appid'] for app in data['applist']['apps'] if app['name'] == game_name]

            try:
                return steam_app_id[0]
            except IndexError:
                print("It doesn't look like that game exists. "
                      "Try ensuring your capitalization matches the game's store page")
        elif game_name == '':
            print("Kindly don't leave the game_name field empty")


def search_workshop_items(search_term, appid, api_key):
    # Construct the URL for the API request
    url = 'https://api.steampowered.com/ISteamRemoteStorage/Search/v1/'
    params = {
        'query': search_term,
        'appid': appid,
        'search_text': 1,
        'key': api_key
    }
    # Make the GET request to the API
    response = requests.get(url, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the publishedfileids from the response
        publishedfileids = [result['publishedfileid'] for result in data['results']]
        return publishedfileids
    else:
        # Return an empty list if the request was not successful
        return []

    # def search_items(self, search_term, app_id, count, start):
    #     url = f'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/' \
    #           f'?appid={app_id}&searchtext={search_term}&count={count}&start={start}&key={self.api_key}'
    #     response = requests.get(url)
    #     return response.json()

    # def search_items(self, search_term, app_id, count, start, sort_by):
    #     url = f'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
    #     payload = {'appid': app_id, 'searchtext': search_term, 'count': count, 'start': start, 'sort_by': sort_by,
    #                'key': self.api_key}
    #     headers = {'Content-Type': 'application/json'}
    #     response = requests.post(url, json=payload, headers=headers)
    #     return response.json()


# initialize SteamWorkshop
api_key = '6AF16629536E86B88E17ADC97FF9808E'
steam_workshop = SteamWorkshop(api_key)

# # find the app id of the game
# game_name = ''  # replace with the name of the game
# app_id = steam_workshop.get_app_id(game_name)
#
# # define search term and criteria
# search_term = 'Monopoly'  # replace with your search term
# count = '10'  # number of items to retrieve
# start = '0'  # index of the first item to retrieve

# data = steam_workshop.search_items(search_term, app_id, count, start)
# print(data)


if __name__ == '__main__':

    app_id = steam_workshop.get_app_id()
    # search_term = 'risk'
    # start = 0
    # count = 5
    #
    # # response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    # # data = response.json()
    # url = f'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/' \
    #       f'?appid=286160&searchtext=risk&childpublishedfileid=0&browsesort=textsearch&section=&actualsort=textsearch'
    #
    # x = requests.post(url)
    # data = x.json()
    # print(data)
    aid = '286160'
    publishedfields = search_workshop_items('risk', aid, api_key)
    print(publishedfields)