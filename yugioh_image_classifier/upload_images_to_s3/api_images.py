import requests
import boto3
import shutil
import os
from yugioh_image_classifier.custom_exceptions.RequestException import ApiRequestError

def upload_api_images_to_s3(bucket_name, endpoint, query_params, response_to_image_urls, count=0):
    """
    :param bucket_name: Name of the s3 bucket images will be stored in
    :type bucket_name: String
    :param endpoint: The api endpoint images will be gathered from
    :type endpoint: String
    :param query_params: Parameters applied to the query call to the api
    :type query_params: Dict
    :param response_to_image_urls: Function to convert the api response into a list of image urls
    :type response_to_image_urls: (Dict) -> List<String>
    :param count: The number of images that have already been downloaded to the given bucket. Used to ensure that every
    image has a unique name.
    :type count: int
    :return: None
    """
    s3 = boto3.client('s3')
    create_bucket_if_not_exists(s3, bucket_name)
    resp = requests.get(endpoint, query_params)

    if resp.status_code != 200:
        raise ApiRequestError('GET request failed with status code {}'.format(resp.status_code))

    image_urls = response_to_image_urls(resp.json())
    dir = 'temporary_image_storage'

    if not os.path.exists(dir):
        os.makedirs(dir)

    for idx, image_url in enumerate(image_urls):
        if (image_url is None):
            print("Image url " + str(idx))
            continue

        # filetype = re.findall("\.[a-zA-z]+", image_url)[-1]
        file_id = str(count + idx)
        filetype = ".jpg"
        filename = 'image' + file_id + filetype
        full_path = dir + '/' + filename

        r = requests.get(image_url, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True
            try:
                with open(full_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    s3.upload_file(full_path, bucket_name, filename)
            except Exception as e:
                print("File {} encounter an error".format(file_id))
                print(e)
        else:
            print("Image url {} failed with response code {}!".format(image_url, r.status_code))

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
