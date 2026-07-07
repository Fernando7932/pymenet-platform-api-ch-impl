from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from src.WorkspaceManagment.infrastructure.controllers.upload_controller import router as upload_router

# Este Resolver de Powertools pertenece SOLO al contexto
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)

# Registramos el router del contexto
app.include_router(upload_router)

@app.get("/")
def health_check():
    return {"status": "success", "context": "WorkspaceManagmentContext"}

def handler(event, context):
    return app.resolve(event, context)
