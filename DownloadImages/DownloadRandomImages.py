import requests
import boto3
import shutil
import os
from UploadFromApiToS3 import upload_api_images_to_s3

bucket = 'random-images2'
endpoint = 'https://picsum.photos/v2/list'
param = {
    'limit': 100,
}

def random_image_processor(response):
    """[summary]

    Args:
        response ([type]): [description]

    Returns:
        [type]: [description]
    """
    image_url_list = []
    for img in response:
        image_url_list.append(img['download_url'])
        
    return image_url_list

if __name__=="__main__":
    upload_api_images_to_s3(bucket, endpoint, param, random_image_processor)