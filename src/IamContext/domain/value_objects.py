from abc import ABC, abstractmethod
import re
from enum import Enum


# ========== EXCEPCIONES DEL DOMINIO ==========

class InvalidEmailError(Exception):
    pass

class CredencialesInvalidasError(Exception):
    pass

class UsuarioBloqueadoError(Exception):
    pass

class EmailYaRegistradoError(Exception):
    pass


# ========== VALUE OBJECTS ==========

class UsuarioId:
    """Wrapper inmutable para el identificador del usuario"""
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("El ID de usuario no puede estar vacío.")
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Email:
    """Value Object que valida y encapsula un email"""
    _EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def __init__(self, direccion: str):
        self._direccion = direccion.strip().lower()
        self._validate()

    @property
    def direccion(self) -> str:
        return self._direccion

    def _validate(self):
        if not self._EMAIL_REGEX.match(self._direccion):
            raise InvalidEmailError(f"El formato de email '{self._direccion}' no es válido.")


class EstadoUsuario(Enum):
    ACTIVO = "ACTIVO"
    BLOQUEADO = "BLOQUEADO"


class CredencialesUsuario:
    """Value Object que encapsula el hash de la contraseña"""
    def __init__(self, hash_contrasena: str):
        self._hash_contrasena = hash_contrasena

    @property
    def hash_contrasena(self) -> str:
        return self._hash_contrasena