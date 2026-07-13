from src.ConversationalAnalytics.domain.value_objects import AnalyticContext, AgentInterface

class AskAgentUseCase:
    # Inyección de dependencias

    def __init__(self, agent_client: AgentInterface):
        self.agent_client = agent_client

    def execute(self, user_query: str, file_uri: str, file_description: str) -> dict:
        # Validaciones + domain logic
        analytic_context = AnalyticContext(user_query, file_uri, file_description)

        # Interface call
        agent_response = self.agent_client.ask(analytic_context)
        return agent_response