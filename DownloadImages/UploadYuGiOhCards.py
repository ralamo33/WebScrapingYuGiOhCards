from DownloadImages.UploadFromApiToS3 import upload_api_images_to_s3

blue_eyes_params = {
    'archetype': 'Blue-Eyes'
}

def yugioh_func (json):
    url_list = []
    for card_data in json.get('data'):
        url_list.append(card_data.get('card_images')[0].get("image_url"))
    return url_list

upload_api_images_to_s3("blue-eyes3", "https://db.ygoprodeck.com/api/v7/cardinfo.php", blue_eyes_params, yugioh_func)