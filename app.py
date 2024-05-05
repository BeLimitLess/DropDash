from flask import Flask, request, render_template, make_response, redirect, url_for, flash
import datetime
import uuid
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings, BlobSasPermissions, generate_blob_sas
from azure.data.tables import TableServiceClient
import hashlib
import secrets
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

load_dotenv()
connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.environ.get("AZURE_STORAGE_CONTAINER")
custom_domain = os.environ.get("AZURE_STORAGE_CUSTOM_DOMAIN")


blob_service_client = BlobServiceClient.from_connection_string(
    connection_string)

table_service_client = TableServiceClient.from_connection_string(
    conn_str=connection_string)
table_client = table_service_client.get_table_client(table_name="cat")


@app.route('/')
def index():
    return render_template('index.html')


def generate_sass(filename_id, expiration):
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name="uploader",
        blob_name=filename_id,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiration
    )
    sas_url = f"{custom_domain}/{container_name}/{filename_id}?{sas_token}"
    return sas_url


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return 'No file part'
    file = request.files['fileInput']
    if file.filename == '':
        return 'No selected file'
    try:
        unique_id = str(uuid.uuid4())
        original_filename = file.filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = unique_id + file_extension
        expire_time = int(request.form.get('expiration', 80))
        print(expire_time)
        start_time = datetime.datetime.now(datetime.timezone.utc)
        expiration_date = start_time + datetime.timedelta(minutes=expire_time)
        password = request.form.get('secret')
        if password != 'null':
            password_hash = hashlib.sha256(password.encode()).hexdigest()
        else:
            password_hash = "null"
        container_client = blob_service_client.get_container_client(
            container_name)
        blob_client = container_client.get_blob_client(unique_filename)
        blob_client.upload_blob(file, overwrite=True, content_settings=ContentSettings(
            content_type=file.content_type))

        entity = {
            'PartitionKey': unique_id,
            'RowKey': unique_id,
            'original_filename': original_filename,
            'secret': password_hash,
            'unique_filename': unique_filename,
            'expire_time': expiration_date
        }
        entity = table_client.create_entity(entity=entity)
        if password != 'null':
            return f"/download/{unique_id}"
        else:
            return generate_sass(unique_filename, expiration_date)

    except Exception as e:
        print(str(e))
        return str(e)


@app.route('/download/<file_id>', methods=['GET', 'POST'])
def download_file(file_id):
    filter = f"PartitionKey eq '{file_id}'"
    entities = table_client.query_entities(filter)
    for entity in entities:
        PasswordHash = entity['secret']
        unique_filename = entity['unique_filename']
        expiration_date = entity['expire_time']
        break

    current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    if current_time > expiration_date:
        return render_template('download.html', file_id=file_id, error='This file has expired.', show_password_field=False)

    if request.method == 'POST':
        entered_password = request.form.get('password')
        if hashlib.sha256(entered_password.encode()).hexdigest() == PasswordHash:
            saslink = generate_sass(unique_filename, expiration_date)
            return render_template('download.html', sas_url=saslink)
        else:
            return render_template('download.html', file_id=file_id, error='Incorrect password. Please try again.', show_password_field=True)

    return render_template('download.html', file_id=file_id, show_password_field=True)


@ app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
