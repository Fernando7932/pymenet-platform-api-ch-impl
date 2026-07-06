from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.DummieContext.application.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])
company_service = CompanyService()

class CreateCompanyRequest(BaseModel):
    name: str
    tax_id: str

@router.post("/", status_code=201)
def create_company(request: CreateCompanyRequest):
    company = company_service.create_company(name=request.name, tax_id=request.tax_id)
    return company

@router.get("/{company_id}")
def get_company(company_id: str):
    company = company_service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
