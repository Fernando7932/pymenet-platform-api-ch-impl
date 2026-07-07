from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from src.ConversationalAnalytics.infrastructure.agent_client import AgentClient
from src.ConversationalAnalytics.application.ask_agent_use_case import AskAgentUseCase

router = Router()
agent_client = AgentClient()
send_use_case = AskAgentUseCase(agent_client=agent_client)

class SendRequest(BaseModel):
    userQuery: str
    fileUri: str
    fileDescription: str

@router.post("/conversational/ask")
def ask_agent():
    """Upload a file to the workspace"""
    request = parse(event=router.current_event.json_body, model=SendRequest)

    result = send_use_case.execute(
        user_query=request.userQuery,
        file_uri=request.fileUri,
        file_description=request.fileDescription
    )

    return result
