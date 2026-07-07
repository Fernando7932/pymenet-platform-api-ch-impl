from src.WorkspaceManagment.domain.value_objects import AnalyticFile, StorageInterface
from google.cloud import storage
import os
import json
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv(override=True)

class GCPStorageClient(StorageInterface):
    def __init__(self):
        gcp_credentials_dict = json.loads(os.getenv('GCP_SA'))
        credentials = service_account.Credentials.from_service_account_info(gcp_credentials_dict)

        self.client = storage.Client(credentials=credentials)
        self.bucket_name = os.getenv('GCP_BUCKET_NAME')

    def upload(self, file: AnalyticFile) -> str:
        bucket = self.client.bucket(self.bucket_name)

        blob = bucket.blob(file.filename)

        blob.upload_from_string(data=file.content, content_type=file.mime_type)

        return f"gs://{self.bucket_name}/{file.filename}"