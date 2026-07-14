from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from src.ConversationalAnalytics.interfaces.rest.send_controller import router as send_router
import os
from dotenv import load_dotenv

# Cargar variables de entorno (para pruebas locales)
load_dotenv(override=True)

# Este Resolver pertenece SOLO al contexto de ConversationalAnalytics
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)

# Registramos el router del contexto
app.include_router(send_router)

@app.get("/")
def health_check():
    return {"status": "success", "context": "ConversationalAnalytics"}

def handler(event, context):
    return app.resolve(event, context)