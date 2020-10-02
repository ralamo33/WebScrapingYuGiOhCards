import requests
import json

card_endpoint = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
staple_card_param = {
    'staple': 'yes'
}

resp = requests.get(card_endpoint)

if resp.status_code != 200:
    raise Exception('GET /tasks/ {}'.format(resp.status_code))

resp_dict = resp.json()
card_data_list = resp_dict.get('data')
image_urls = []

for card_data in card_data_list:
    image_urls.append(card_data.get('card_images')[0].get("image_url"))


