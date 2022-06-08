import os
from azure.storage.blob import BlobClient, ContentSettings

connection_string = "DefaultEndpointsProtocol=https;AccountName=soilsamples;AccountKey=Q4mp30h+EtmMzNxZosJEvKaQCpaKG+Y3MF/fITKSwnsTG8Z2/8DbaCnjWwPvDO/tU+zN8VCtTsas+AStNTlxgA==;EndpointSuffix=core.windows.net"
container_name = "soilsensor1"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

def upload_to_azure_blob(filename: str):
    # upload image to azure blob storage
    blob_name = filename
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name = blob_name)
    image_content_setting = ContentSettings(content_type='image/jpeg')
    with open(os.path.join(APP_STATIC, blob_name), "rb") as data:
        blob.upload_blob(data, overwrite = True, content_settings=image_content_setting)
    print("Upload complete")
    #return send_file(filename, mimetype='image/jpg')
    return None
    
def read_boolean_from_file(filename: str):
    if not os.path.isfile(filename):
        _write_boolean_to_file(filename, False)
        return False

    with open(filename, "r") as file:
        try:
            state = bool(int(file.read()))
        except ValueError:
            # logger.warning("Error reading file")
            state = False
    return state

def write_boolean_to_file(filename: str, state: bool):
    with open(filename, "w") as file:
        file.write(str(int(state)))
