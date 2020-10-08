import requests
import boto3
import shutil
import os

s3_client = boto3.client('s3')
s3_resource = boto3.client('s3')
bucket_name = 'random-images'

# If the bucket already exists, this will return it
bucket = s3.create_bucket(Bucket=bucket_name)

endpoint = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

resp = requests.get(card_endpoint)

if resp.status_code != 200:
    raise Exception('GET /tasks/ {}'.format(resp.status_code))

resp_dict = resp.json()
card_data_list = resp_dict.get('data')
image_urls = []
dir = 'card_images/dark_magician'

if not os.path.exists(dir):
    os.makedirs(dir)

for card_data in card_data_list:
    image_urls.append(card_data.get('card_images')[0].get("image_url"))

for image_url in image_urls:
    filename = dir + '/' + image_url.split("/")[-1]

    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            # s3.upload_file(filename, bucket, filename)

print('yuGiOh cards uploaded to s3 bucket {}'.format(bucket))
shutil.rmtree(dir)
