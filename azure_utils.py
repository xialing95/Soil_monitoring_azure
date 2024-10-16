import os
import asyncio
import aiohttp
from azure.storage.blob.aio import BlobClient

connection_string = ""
container_name = ""

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

async def upload_to_azure_blob(filename: str):
    # upload image to azure blob storage
    blob_name = filename
    blob_client = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name = blob_name)
    async with blob_client as blob:
    #image_content_setting = ContentSettings(content_type='image/jpeg')
        with open(os.path.join(APP_STATIC, blob_name), "rb") as data:
            await blob.upload_blob(data, overwrite = True)
    print(filename + " upload complete")
    #return send_file(filename, mimetype='image/jpg')
