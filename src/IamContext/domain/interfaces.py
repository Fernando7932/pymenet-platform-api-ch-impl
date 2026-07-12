from abc import ABC, abstractmethod
from src.IamContext.domain.entities import Usuario


class UserRepositoryInterface(ABC):
    """
    Contrato del repositorio de usuarios.
    El dominio DEFINE lo que necesita, la infraestructura lo IMPLEMENTA.
    """

    @abstractmethod
    def find_by_email(self, email: str) -> Usuario | None:
        """Busca un usuario por email. Retorna None si no existe."""
        pass

    @abstractmethod
    def save(self, usuario: Usuario) -> None:
        """Persiste un usuario nuevo en el almacenamiento."""
        pass
