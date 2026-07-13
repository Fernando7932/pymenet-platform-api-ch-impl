from typing import Enum

class Email:
    """Valida formato de email"""
    def __init__(self, direccion: str):
        self._direccion = direccion
        self._validate()

    @property
    def direccion(self) -> str: ...

    def _validate(self): ...  # regex de email

class EstadoUsuario(Enum):
    ACTIVO = "ACTIVO"
    BLOQUEADO = "BLOQUEADO"

class UsuarioId:
    """Wrapper inmutable para el ID"""
    def __init__(self, value: str): ...

class CredencialesUsuario:
    """Encapsula el hash de la contraseña"""
    def __init__(self, hash_contrasena: str): ...

    def verificar(self, plain_password: str) -> bool:
        """Compara la contraseña plana contra el hash"""
        ...
