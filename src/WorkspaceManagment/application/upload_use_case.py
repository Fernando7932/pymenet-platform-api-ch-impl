from src.WorkspaceManagment.domain.value_objects import AnalyticFile, StorageInterface

class UploadUseCase:
    def __init__(self, storage_client: StorageInterface):
        self.storage_client = storage_client

    def execute(self, filename: str, content: bytes, mime_type: str, description: str) -> dict:
        analytic_file = AnalyticFile(filename, content, mime_type, description)

        file_uri = self.storage_client.upload(analytic_file)

        return {
            "fileUri": file_uri,
            "fileDescription": analytic_file.description,
            "fileName": analytic_file.filename
        }