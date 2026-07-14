from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from src.ConversationalAnalytics.infrastructure.agent_client import AgentClient
from src.ConversationalAnalytics.application.ask_agent_use_case import AskAgentUseCase
from src.common.auth_middleware import verify_jwt_token
import logging

logger = logging.getLogger(__name__)

router = Router()
agent_client = AgentClient()
send_use_case = AskAgentUseCase(agent_client=agent_client)

class SendRequest(BaseModel):
    userQuery: str
    fileUri: str
    fileDescription: str

@router.post("/conversational/ask")
def ask_agent():
    """Consultar al agente de IA (Ruta protegida)"""
    # Verificación JWT — si falla, retorna inmediatamente
    try:
        verify_jwt_token(router.current_event.raw_event)
    except PermissionError as e:
        return {"statusCode": 401, "message": str(e)}

    # Parseo del body
    try:
        request = parse(event=router.current_event.json_body, model=SendRequest)
    except Exception as e:
        logger.error(f"Error parsing request: {e}")
        return {"statusCode": 400, "message": f"Request inválido: {str(e)}"}

    # Ejecución del caso de uso
    try:
        result = send_use_case.execute(
            user_query=request.userQuery,
            file_uri=request.fileUri,
            file_description=request.fileDescription
        )
        return result
    except Exception as e:
        logger.error(f"Error calling agent: {e}")
        return {"statusCode": 500, "message": f"Error interno del agente: {str(e)}"}
