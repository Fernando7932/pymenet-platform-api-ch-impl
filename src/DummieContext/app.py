from fastapi import FastAPI
from mangum import Mangum
from src.DummieContext.infrastructure.controllers.company_controller import router as company_router


# Este FastAPI pertenece SOLO al DummieContext (Companies)
app = FastAPI(
    title="Pymenet API - Company Context",
    description="API Serverless para el Bounded Context de Empresas",
    version="1.0.0",
    # Opcional: configurar root_path si quieres que Swagger entienda que está detrás de /companies
    # root_path="/dev/companies">
)

app.include_router(company_router)

@app.get("/")
def health_check():
    return {"status": "ok", "context": "CompanyContext"}

handler = Mangum(app)
