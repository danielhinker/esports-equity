"""Custom S3 storage backends to store files in subfolders."""
from storages.backends.s3boto import S3BotoStorage

class MediaRootS3BotoStorage(S3BotoStorage):
    location = 'media'