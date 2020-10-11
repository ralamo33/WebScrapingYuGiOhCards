from DownloadImages.UploadFromApiToS3 import upload_api_images_to_s3

query_params = {}

def yugioh_func (json):
    url_list = []
    for card_data in json.get('data'):
        url_list.append(card_data.get('card_images')[0].get("image_url"))
    return url_list

upload_api_images_to_s3("blue-eyes4", "https://db.ygoprodeck.com/api/v7/cardinfo.php", query_params, yugioh_func)