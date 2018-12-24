def upload(file_path, filename, content_type):
    with open(file_path) as file_stream:
        client = _get_storage_client()
        bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
        blob = bucket.blob(filename)

        blob.upload_from_string(
            file_stream,
            content_type=content_type)

        url = blob.public_url

        if isinstance(url, six.binary_type):
            url = url.decode('utf-8')

        return url

def _get_storage_client():
    return storage.Client(
        project=current_app.config['PROJECT_ID'])