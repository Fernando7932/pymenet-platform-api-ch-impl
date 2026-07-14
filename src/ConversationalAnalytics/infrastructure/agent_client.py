import os
import requests
from src.ConversationalAnalytics.domain.value_objects import AgentInterface
from src.ConversationalAnalytics.domain.value_objects import AnalyticContext
import uuid
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
import google.auth.transport.requests

load_dotenv(override=True)

class AgentClient(AgentInterface):
    def __init__(self):
        self._cloud_run_url = os.getenv('AGENT_URL')
        if not self._cloud_run_url:
            raise ValueError("La URL del agente de Cloud Run no está configurada.")

        # Autenticación OIDC para Cloud Run
        gcp_credentials_dict = json.loads(os.getenv('GCP_SA'))
        self._credentials = service_account.IDTokenCredentials.from_service_account_info(
            gcp_credentials_dict,
            target_audience=self._cloud_run_url
        )

    def _get_auth_token(self) -> str:
        """Genera y refresca el Identity Token (JWT) firmado por Google"""
        auth_req = google.auth.transport.requests.Request()
        self._credentials.refresh(auth_req)
        return self._credentials.token

    def ask(self, context: AnalyticContext) -> dict:
        url = f"{self._cloud_run_url}/run"

        prompt = f"""
        userQuery: {context.user_query}
        fileUri: {context.file_uri}
        fileDescription: {context.file_description}
        """

        payload = {
            "app_name": f"{os.getenv('AGENT_NAME')}",
            "user_id": f"{uuid.uuid4()}",
            "session_id": f"{uuid.uuid4()}",
            "new_message": {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self._get_auth_token()}"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)

        response.raise_for_status()
        raw_data = response.json()

        # Extraer solo la respuesta final del agente
        final_answer = "No se pudo obtener una respuesta del agente."

        # Recorremos la lista de atrás hacia adelante para encontrar el último texto generado
        if isinstance(raw_data, list):
            for step in reversed(raw_data):
                if "content" in step and "parts" in step["content"]:
                    for part in step["content"]["parts"]:
                        if "text" in part:
                            final_answer = part["text"]
                            break
                if final_answer != "No se pudo obtener una respuesta del agente.":
                    break

        return {
            "answer": final_answer
        }