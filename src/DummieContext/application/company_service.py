from src.DummieContext.domain.company import Company

class CompanyService:
    def __init__(self):
        # Aquí inyectaríamos el repositorio en un escenario real (ej. CompanyRepository)
        pass

    def create_company(self, name: str, tax_id: str) -> Company:
        # Lógica de negocio (ej. validaciones, verificar reglas de negocio)
        company = Company(name=name, tax_id=tax_id)
        # self.repository.save(company)
        return company

    def get_company(self, company_id: str) -> Company:
        # Lógica para obtener de infraestructura
        # Retornamos un dummie por ahora
        return Company(id=company_id, name="Empresa Dummie", tax_id="123456789")
