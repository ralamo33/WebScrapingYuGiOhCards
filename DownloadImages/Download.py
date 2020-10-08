import requests
import boto3
import shutil
import os

'''
Download images to an s3 bucket. 
bucket_name: (String): Name of the s3 bucket images will be stored in
endpoint: (String): The api endpoint being used to gather images
query_params: (Dict): Paramaters used to filter the api response
response_to_image_urls: (Function): Recieves the api response, and converts it into a list of image urls
'''
def download_images_s3(bucket_name, endpoint, query_params, json_to_image_urls):
    s3 = boto3.client('s3')
    create_bucket_if_not_exists(s3, bucket_name)
    resp = requests.get(endpoint, query_params)

    if resp.status_code != 200:
        raise Exception('GET request failed with status code {}'.format(resp.status_code))

    image_urls = json_to_image_urls(resp.json())
    dir = 'temporary_image_storage'

    if not os.path.exists(dir):
        os.makedirs(dir)

    for image_url in image_urls:
        filename = dir + '/' + image_url.split("/")[-1]

        r = requests.get(image_url, stream = True)

        if r.status_code == 200:
            r.raw.decode_content = True

            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    shutil.rmtree(dir)



def create_bucket_if_not_exists(client, bucket_name):
    bucket_exists = False
    bucket_list = client.list_buckets()['Buckets']
    for bucket in bucket_list:
        if bucket['Name'] == bucket_name:
            bucket_exists = True
            break
    if not bucket_exists:
        client.create_bucket(Bucket=bucket_name)

blue_eyes_params = {
    'archetype': 'Blue-Eyes'
}

def yugioh_func (json):
    url_list = []
    for card_data in json.get('data'):
        url_list.append(card_data.get('card_images')[0].get("image_url"))
    return url_list

download_images_s3("blue-eyes2", "https://db.ygoprodeck.com/api/v7/cardinfo.php", blue_eyes_params, yugioh_func)