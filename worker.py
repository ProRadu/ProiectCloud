import os
import zipfile
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobClient, ContainerClient, BlobServiceClient
from googletrans import Translator

# Azure Blob Storage account information
storage_account_key = "dummy"
storage_account_name = "dummy"
connection_string = "dummy"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

client = CosmosClient("dummy", "dummy")

# name of the container where the .zip files are stored
zip_container_name = "netradus"

# name of the container where the translated text will be stored
translated_container_name = "text_tradus"

# create a ContainerClient object for the container where the .zip files are stored
zip_container_client = blob_service_client.get_container_client(zip_container_name)

database_id = "websiteDB"


database_client = client.get_database_client(database_id)
translated_container_client = database_client.get_container_client(translated_container_name)


# function to translate text using a free translation library
def translate_text(text,source_language,target_language):
    translator = Translator()
    translated_text = translator.translate(text,src=source_language, dest=target_language).text

    return translated_text

while True:
    # list the .zip files in the container
    zip_files = list(zip_container_client.list_blobs())

    # loop through the .zip files
    for zip_file in zip_files:
        # get the name of the .zip file
        zip_file_name = zip_file.name

        # check if the .zip file has already been translated
        query = "SELECT * FROM c WHERE c.zip_file_name = @zip_file_name"
        parameters = [{"name": "@zip_file_name", "value": zip_file_name}]
        translated_items = list(translated_container_client.query_items(query=query, parameters=parameters,enable_cross_partition_query=True))

        # if the .zip file has not been translated, translate it and save the translated text to the database
        if not translated_items:
            # download the .zip file from the container
            with open("temp.zip", "wb") as f:
                f.write(zip_container_client.download_blob(blob=zip_file).readall())

            # extract the .txt files from the .zip file
            with zipfile.ZipFile("temp.zip", "r") as zip_ref:
                zip_ref.extractall("temp")

            # loop through the .txt files
            for file in os.listdir("temp"):
                # open the .txt file
                with open(f"temp/{file}", "r") as f:
                    # read the contents of the .txt file
                    text = f.read()

                # translate the text
                translated_text = translate_text(text,"en","ro")

                # create an item in the database with the translated text
                data = {
                    'id': file,
                    'originalText': text,
                    'translatedText': translated_text,
                    'language': 'Romanian'
                }

                translated_container_client.upsert_item(data)
                #zip_container_client.delete_blob(blob=zip_file)
            # delete the extracted .txt files and the downloaded .zip file
            os.remove("temp.zip")
            for file in os.listdir("temp"):
                os.remove(f"temp/{file}")
            os.rmdir("temp")