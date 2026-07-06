from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from src.DummieContext.application.company_service import CompanyService

router = Router()
company_service = CompanyService()

class CreateCompanyRequest(BaseModel):
    name: str
    tax_id: str

@router.post("/companies")
def create_company():
    # Extraemos el payload validado con Pydantic directamente del evento
    request = parse(event=router.current_event.json_body, model=CreateCompanyRequest)

    company = company_service.create_company(name=request.name, tax_id=request.tax_id)
    # Convertimos la respuesta a diccionario para Powertools
    return company.model_dump()

@router.get("/companies/<company_id>")
def get_company(company_id: str):
    company = company_service.get_company(company_id)
    if not company:
        raise NotFoundError("Company not found")
    return company.model_dump()
