from fastapi import FastAPI
from mangum import Mangum
from src.DummieContext.infrastructure.controllers.company_controller import router as company_router

app = FastAPI(
    title="Pymenet API Dummie",
    description="API Serverless con FastAPI y Arquitectura DDD",
    version="1.0.0"
)

# Registramos los routers de los Bounded Contexts
app.include_router(company_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Pymenet API is running"}

# Mangum actúa como adaptador para AWS Lambda + API Gateway
handler = Mangum(app)
