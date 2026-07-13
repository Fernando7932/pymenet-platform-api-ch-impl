from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.utilities.parser import parse, BaseModel
from src.IamContext.infrastructure.dynamo_user_repository import DynamoUserRepository
from src.IamContext.infrastructure.jwt_service import JWTService
from src.IamContext.application.login_use_case import LoginUseCase
from src.IamContext.application.register_use_case import RegisterUseCase
from src.IamContext.domain.value_objects import (
    CredencialesInvalidasError, UsuarioBloqueadoError,
    InvalidEmailError, EmailYaRegistradoError
)

router = Router()

# Composition Root: inyección de dependencias
user_repository = DynamoUserRepository()
jwt_service = JWTService()
login_use_case = LoginUseCase(user_repository=user_repository)
register_use_case = RegisterUseCase(user_repository=user_repository)


# ========== REQUEST MODELS ==========

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    nombre: str
    email: str
    password: str


# ========== ENDPOINTS ==========

@router.post("/auth/login")
def login():
    """Endpoint público: iniciar sesión y obtener JWT"""
    request = parse(event=router.current_event.json_body, model=LoginRequest)

    try:
        user_data = login_use_case.execute(
            email=request.email,
            password=request.password
        )

        # Generar JWT con los datos del usuario
        token = jwt_service.generate_token(user_data)

        return {
            "token": token,
            "user": user_data
        }

    except CredencialesInvalidasError:
        return {"statusCode": 401, "message": "Credenciales incorrectas."}
    except UsuarioBloqueadoError:
        return {"statusCode": 403, "message": "El usuario se encuentra bloqueado."}


@router.post("/auth/register")
def register():
    """Endpoint público: registrar un usuario nuevo"""
    request = parse(event=router.current_event.json_body, model=RegisterRequest)

    try:
        user_data = register_use_case.execute(
            nombre=request.nombre,
            email=request.email,
            password=request.password
        )

        # Generar JWT automáticamente al registrarse
        token = jwt_service.generate_token(user_data)

        return {
            "token": token,
            "user": user_data
        }

    except EmailYaRegistradoError as e:
        return {"statusCode": 409, "message": str(e)}
    except InvalidEmailError as e:
        return {"statusCode": 400, "message": str(e)}
