from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from src.WorkspaceManagment.infrastructure.controllers.upload_controller import router as upload_router

# Este Resolver de Powertools pertenece SOLO al DummieContext
app = APIGatewayRestResolver()

# Registramos el router del contexto
app.include_router(upload_router)

@app.get("/")
def health_check():
    return {"status": "success", "context": "WorkspaceManagmentContext"}

def handler(event, context):
    return app.resolve(event, context)
