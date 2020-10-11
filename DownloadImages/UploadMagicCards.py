from DownloadImages.UploadFromApiToS3 import upload_api_images_to_s3

endpoint = "https://api.magicthegathering.io/v1/cards"
bucket = "magic-cards2"

def extract_magic_card_urls (json):
    url_list = []
    for card_data in json.get('cards'):
        url_list.append(card_data.get('imageUrl'))
    return url_list

upload_api_images_to_s3(bucket, endpoint, {}, extract_magic_card_urls)
