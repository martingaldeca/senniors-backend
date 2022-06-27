from storages.backends.s3boto3 import S3Boto3Storage

from backend import settings


class MediaStorage(S3Boto3Storage):
    default_acl = 'public-read'
    location = settings.MEDIA_ROOT
    file_overwrite = False
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    querystring_auth = False


class StaticStorage(S3Boto3Storage):
    default_acl = 'public-read'
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    querystring_auth = False
    file_overwrite = False
