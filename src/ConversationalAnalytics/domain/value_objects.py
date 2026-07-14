from abc import ABC, abstractmethod

class EmptyQueryError(Exception):
    pass

class AnalyticContext:
    def __init__(self, user_query: str, file_uri: str, file_description: str):
        self._validate(user_query, file_uri)
        self._user_query = user_query
        self._file_uri = file_uri
        self._file_description = file_description

    # Getters
    @property
    def user_query(self) -> str:
        return self._user_query

    @property
    def file_uri(self) -> str:
        return self._file_uri

    @property
    def file_description(self) -> str:
        return self._file_description

    # Validaciones
    def _validate(self, user_query: str, file_uri: str):
        if not user_query or not user_query.strip():
            raise EmptyQueryError("La pregunta de negocio no puede estar vacía.")
        if not file_uri.startswith("gs://"):
            raise ValueError("La URI del archivo debe ser un formato válido de Google Storage (gs://).")

# EL CONTRATO (El "Qué" necesita el dominio)
class AgentInterface(ABC):
    @abstractmethod
    def ask(self, context: AnalyticContext) -> dict:
        """Envía el contexto al Agente IA y retorna la respuesta procesada."""
        pass