from storages.backends.s3boto3 import S3Boto3Storage

__all__ = (
    'S3DefaultStorage',
    'DefaultFilesStorage',
)


class S3DefaultStorage(S3Boto3Storage):
    location = 'media'


class DefaultFilesStorage(S3Boto3Storage):
    location = 'media'
