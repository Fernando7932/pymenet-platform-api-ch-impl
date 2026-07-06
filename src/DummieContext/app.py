from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from src.DummieContext.infrastructure.controllers.company_controller import router as company_router

# Este Resolver de Powertools pertenece SOLO al DummieContext
app = APIGatewayRestResolver()

# Registramos el router del contexto
app.include_router(company_router)

@app.get("/")
def health_check():
    return {"status": "ok", "context": "CompanyContext"}

def handler(event, context):
    return app.resolve(event, context)
