from flask import Flask, render_template, request
from azure.storage.blob import ContainerClient, BlobClient, BlobServiceClient, ResourceTypes
from azure.cosmos import CosmosClient
import zipfile

app = Flask(__name__)





@app.route('/upload', methods=['GET','POST'])
def upload():
    storage_account_key = "dummy"
    storage_account_name = "dummy"
    connection_string = "dummy"
    container_name = "netradus"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    if request.method == 'POST':
        file = request.files['file']
        file_name=file.filename
        blob_client = blob_service_client.get_blob_client(container=container_name,blob=file_name)

        blob_client.upload_blob(file)

    return render_template('upload.html')


@app.route('/translated', methods=['GET'])
def translated():
    client = CosmosClient("dummy",
                          "dummy")

    database_id = "websiteDB"
    container_id = "text_tradus"

    database_client = client.get_database_client(database_id)
    container_client = database_client.get_container_client(container_id)

    # Query the container for all translated texts
    query = "SELECT * FROM c"
    texts = list(container_client.query_items(query=query, enable_cross_partition_query=True))

    # Render the results on the page
    return render_template("translated.html", texts=texts)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8075)
