import boto3

'''
Clears a bucket of all files and then deletes it
bucket_name (String): Name of bucket to be deleted
'''
def delete_bucket(bucket_name):
    clear_bucket(bucket_name)
    client = boto3.client("s3")
    client.delete_bucket(Bucket=bucket_name)


'''
Clears a bucket of all files
bucket_name (String): Name of the bucket user wants to clear
'''
def clear_bucket(bucket_name):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    keys = get_bucket_object_keys(bucket, limit=1000)
    while len(keys) != 0:
        resp = delete_objects_from_bucket(bucket, keys)
        keys = get_bucket_object_keys(bucket, limit=1000)
        if not "Deleted" in resp:
            break

'''
bucket (s3.Bucket): Bucket that objects will be deleted from
keys: (List of String): Keys of the objects to be deleted
return (Dict): The response from AWS to the delete request
'''
def delete_objects_from_bucket(bucket, keys):
    key_dictionary_list = []
    for key in keys:
        key_dictionary_list.append({'Key': key})
    delete = {
        'Objects': key_dictionary_list,
    }
    return bucket.delete_objects(Delete=delete, RequestPayer='requester')


'''
Returns a list of python object keys.
bucket: (s3.Bucket): This is where object keys will be pulled from
limit: Returns the first limit object keys
'''
def get_bucket_object_keys(bucket, limit=1000000):
    keys = []
    for idx, obj in enumerate(bucket.objects.all()):
        keys.append(obj.key)
        if idx == limit:
            break
    return keys