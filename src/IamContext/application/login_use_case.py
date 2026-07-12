from src.IamContext.domain.interfaces import UserRepositoryInterface
from src.IamContext.domain.value_objects import CredencialesInvalidasError


class LoginUseCase:
    """Orquesta el flujo de inicio de sesión"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository

    def execute(self, email: str, password: str) -> dict:
        # 1. Buscar usuario por email
        usuario = self._user_repository.find_by_email(email)
        if usuario is None:
            raise CredencialesInvalidasError("Las credenciales son incorrectas.")

        # 2. Ejecutar lógica de dominio (validar estado + contraseña)
        usuario.iniciar_sesion(password)

        # 3. Retornar datos del usuario (el JWT se genera en el controlador)
        return {
            "user_id": usuario.id.value,
            "nombre": usuario.nombre,
            "email": usuario.email.direccion
        }
