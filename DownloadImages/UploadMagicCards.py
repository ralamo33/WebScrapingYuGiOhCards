from DownloadImages.UploadFromApiToS3 import upload_api_images_to_s3

endpoint = "https://api.magicthegathering.io/v1/cards"
bucket = "magic-cards2"


def extract_magic_card_urls(json):
    url_list = []
    for card_data in json.get('cards'):
        url_list.append(card_data.get('imageUrl'))
    return url_list


if __name__ == "__main__":
    params = {
        'contains': 'imageUrl',
    }

    # Each call to magic the gathering responds with only 100 cards, so to get 10,000 cards, we need 100 calls
    for page in range(100):
        print(page)
        params['page'] = page
        upload_api_images_to_s3(bucket, endpoint, params, extract_magic_card_urls, page * 100)
