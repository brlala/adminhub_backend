"""
Manager for all operations related to cloud services. Eg. Uploading files to S3 buckets.
All related helpers should go here.
"""
import logging
import mimetypes
import os
import sys
import threading
from urllib.parse import quote

import boto3
from fastapi import UploadFile

from app.server.core.env_variables import local_config


class ProgressPercentage(object):
    """
    Print percentage for fileupload
    """

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


async def upload_file_implementation(file: UploadFile, *, folder: str = None, new_filename: str = None) -> str:
    """
    Upload a file to a bucket
    <call method> upload_file_implementation(file, , bucket_path='temporary/data')

    :param file: fileobject passed down by FastAPI type
    :param folder: Location you want to put your files, on the cloud etc. 'temporary/data'
    :param new_filename: custom rename file when uploading to bucket
    :return: URL of file location
    """
    bucket_name = local_config.CLOUD_BUCKET_NAME

    filename = new_filename if new_filename else file.filename
    # bucket path is the key(url) for the file when uploaded
    file_path = 'portal/flows/' + f"{filename if not folder else f'{folder}/{filename}'}"
    url = ""

    cloud_provider = local_config.CLOUD_PROVIDER
    cloud_url = local_config.CLOUD_BUCKET_URL
    cloud_bucket = local_config.CLOUD_BUCKET_NAME

    if cloud_provider == "aws" and await upload_file_aws(file, bucket_name, file_path):
        url = f'{cloud_url.format(cloud_bucket)}{quote(file_path)}'
    # elif cloud_provider == "alibaba":
    #     if upload_file_alibaba(bucket_name, relative_path, bucket_path, content_type=content_type):
    #         url = f"{cloud_url.format(cloud_bucket)}{quote(bucket_path)}"
    # else:
    #     logger.exception(f"Invalid 'cloud_provider': {cloud_provider}")
    #     return url

    return url


#
#
# def create_presigned_url_aws(bucket, filename, expiration):
#     """
#     Creates a url accessible for a limited time. Requires private s3 bucket
#     :param bucket: bucket name
#     :param filename: filename in bucket
#     :param expiration: amount of time before expiration in seconds
#     :return: returns presigned URL, modifying headers does not extend expiry time or access the file 'illegally'
#     e.g. https://repository.s3.amazonaws.com/folder/{filename}?AWSAccessKeyId={key}Signature={signature}Expires={expire}
#     """
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': bucket,
#                                                             'Key': filename},
#                                                     ExpiresIn=expiration
#                                                     )
#     except ClientError:
#         logger.error(f'Error generating presigned URL bucket: {bucket}, file: {filename}')
#         return None
#
#     return response


async def upload_file_aws(file: UploadFile, bucket_name: str, file_path: str) -> bool:
    """
    Upload a file to an S3 bucket
    :param file: file of type FastAPI
    :param bucket_name: Bucket to upload to
    :param file_path: S3 object name path
    :return: True if file was uploaded, else False
    """
    extras = {"ContentType": file.content_type}

    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=local_config.CLOUD_ACCESS_KEY,
        aws_secret_access_key=local_config.CLOUD_SECRET_ACCESS_KEY
    )

    try:
        response = s3_client.upload_fileobj(file.file, bucket_name, file_path, ExtraArgs=extras)
        logging.info(f'S3 file upload response: {response}')
    except Exception as e:
        print('error')
        logging.error(e)
        return False
    return True
#
#
# def upload_file_alibaba(bucket_name: str, relative_path: str, bucket_path: str, *, content_type: str = None) -> bool:
#     """
#     Upload a file to alibaba cloud bucket
#     :return: True if file was uploaded, else False
#     """
#     if content_type is None:
#         content_type = oss2.utils.content_type_by_name(relative_path)
#     headers = {"Content-Type": content_type}
#
#     auth = oss2.Auth(gv.chatbot_config["cloud_access_key_id"], gv.chatbot_config["cloud_secret_access_key"])
#     bucket = oss2.Bucket(auth, gv.chatbot_config["cloud_storage_url"].replace("{}.", ""), bucket_name)
#     try:
#         result = bucket.put_object_from_file(bucket_path, relative_path, headers)
#         print(f'Upload status: {result.status}')
#         return True
#     except Exception as e:
#         logging.error(e)
#         return False
