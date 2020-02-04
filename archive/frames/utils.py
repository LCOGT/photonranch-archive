import boto3
from functools import lru_cache
from django.conf import settings
from datetime import timedelta


@lru_cache(maxsize=1)
def get_s3_client():
    config = boto3.session.Config(region_name='us-west-2', signature_version='s3v4')
    return boto3.client('s3', config=config)


def remove_dashes_from_keys(dictionary):
    new_dictionary = {}
    for k in dictionary:
        new_key = k.replace('-', '_')
        new_dictionary[new_key] = dictionary[k]
    return new_dictionary


def fits_keywords_only(dictionary):
    new_dictionary = {}
    for k in dictionary:
        if k[0].isupper():
            new_dictionary[k] = dictionary[k]
    return new_dictionary


def build_nginx_zip_text(frames, directory, uncompress=False):
    '''
    Build a text document in the format required by the NGINX mod_zip module
    so that NGINX will automatically build and stream a ZIP file to the client.

    For more information, please refer to:
    https://www.nginx.com/resources/wiki/modules/zip/

    @frames: a List of Frame objects
    @directory: the directory within the ZIP file to place the files
    @uncompress: automatically uncompress the files for the client

    @return: text document in NGINX mod_zip format
    '''
    client = get_s3_client()
    ret = []

    for frame in frames:
        # retrieve the database record for the Version we will fetch
        version = frame.version_set.first()
        # default location (return files as-is from AWS S3 Bucket)
        location = '/s3-native/{}/'.format(version.id)
        # if the user requested that we uncompress the files, then redirect through
        # our transparent funpacker
        if uncompress:
            location = '/s3-funpack/{}/'.format(version.id)

        # The NGINX mod_zip module builds ZIP files using a manifest. Build the manifest
        # line for this frame.
        line = '- {size} {location} {directory}/{basename}{extension}\n'.format(
            size=version.size,
            location=location,
            directory=directory,
            basename=frame.basename,
            extension=version.extension,
        )
        # Add to returned lines
        ret.append(line)

    # Concatenate all lines together into a single string
    return ''.join(ret)
