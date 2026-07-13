from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from src.WorkspaceManagment.infrastructure.gcp_storage_client import GCPStorageClient
from src.WorkspaceManagment.application.upload_use_case import UploadUseCase
from src.common.auth_middleware import verify_jwt_token

router = Router()
gcp_storage_client = GCPStorageClient()
upload_use_case = UploadUseCase(storage_client=gcp_storage_client)

class UploadFileRequest(BaseModel):
    filename: str
    content: bytes
    mime_type: str
    description: str

@router.post("/workspace/upload")
def upload_file():
    """Upload a file to the workspace (Ruta protegida)"""
    try:
        verify_jwt_token(router.current_event.raw_event)
    except PermissionError as e:
        return {"statusCode": 401, "message": str(e)}

    request = parse(event=router.current_event.json_body, model=UploadFileRequest)

    result = upload_use_case.execute(
        filename=request.filename,
        content=request.content,
        mime_type=request.mime_type,
        description=request.description
    )

    return result
