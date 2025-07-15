'''
This module provides functions for uploading and downloading files to/from
Google Cloud Storage buckets, with support for multiple authentication methods.
ATTENTION: must be edited only in the shared directory.
'''

import os
from google.cloud import storage  # type: ignore[import-untyped]
from google.cloud.exceptions import GoogleCloudError  # type: ignore[import-untyped]
from dotenv import load_dotenv

# Load environment variables at the top of the file
load_dotenv()

# Get bucket name from environment variable
BUCKET_NAME = os.getenv('BUCKET_NAME')
if not BUCKET_NAME:
    raise RuntimeError('BUCKET_NAME environment variable is required.')

if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    print('Using credentials from GOOGLE_APPLICATION_CREDENTIALS')
    storage_client = storage.Client()
elif os.getenv('K_SERVICE'):
    print('Using Application Default Credentials (ADC).')
    storage_client = storage.Client()
else:
    raise RuntimeError('No Google Cloud credentials found. Set GCP_* environment variables or GOOGLE_APPLICATION_CREDENTIALS.')


def download_from_gcs(remote_path: str):
    '''Downloads a file from GCS to /tmp and returns the local path.'''
    try:     
        blobname = remote_path

        local_path = f'/tmp/{os.path.basename(blobname)}'
        bucket = storage_client.bucket(BUCKET_NAME)  # type: ignore[misc]
        blob = bucket.blob(blobname)  # type: ignore[misc]
        blob.download_to_filename(local_path)  # type: ignore[misc]

        print(f'Downloaded {blobname} from {BUCKET_NAME} to {local_path}')
        return local_path
    except GoogleCloudError as e:
        print(f'Failed to download {remote_path}: {e}')
        raise


def upload_to_gcs(local_path: str, dirname: str, filename: str):
    '''Uploads a file to GCS.'''
    try:
        blobname = os.path.join(dirname, filename)
        bucket = storage_client.bucket(BUCKET_NAME)  # type: ignore[misc]
        blob = bucket.blob(blobname)  # type: ignore[misc]
        blob.upload_from_filename(local_path)  # type: ignore[misc]

        print(f'File {local_path} uploaded to {BUCKET_NAME}/{blobname}.')
        return True
    except GoogleCloudError as e:
        print(f'Failed to upload {local_path} to GCS: {e}')
        return False

