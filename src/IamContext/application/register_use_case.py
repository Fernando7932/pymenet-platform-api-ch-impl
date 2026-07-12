import uuid
from src.IamContext.domain.interfaces import UserRepositoryInterface
from src.IamContext.domain.entities import Usuario
from src.IamContext.domain.value_objects import EmailYaRegistradoError


class RegisterUseCase:
    """Orquesta el flujo de registro de un usuario nuevo"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository

    def execute(self, nombre: str, email: str, password: str) -> dict:
        # 1. Verificar que el email no esté registrado
        existing_user = self._user_repository.find_by_email(email)
        if existing_user is not None:
            raise EmailYaRegistradoError(f"El email '{email}' ya está registrado.")

        # 2. Crear el usuario usando el Factory Method del dominio
        usuario = Usuario.registrar(
            id_value=str(uuid.uuid4()),
            nombre=nombre,
            email_str=email,
            plain_password=password
        )

        # 3. Persistir en el repositorio
        self._user_repository.save(usuario)

        # 4. Retornar confirmación
        return {
            "user_id": usuario.id.value,
            "nombre": usuario.nombre,
            "email": usuario.email.direccion
        }
