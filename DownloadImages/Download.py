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
def download_images_s3(bucket_name, endpoint, query_params, response_to_image_urls):
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    s3_client.list_buckets()

'''
Returns an s3 bucket of the given name. Creates the bucket if it does not already exist.
'''
def create_bucket_if_not_exists(client, resource, bucket_name):
    bucket_exists = false
    for bucket in client.list_buckets():
        if bucket == bucket_name:
            bucket_exists = true
            break;
    if not bucket_exists:

