from abc import ABC, abstractmethod
import os

class InvalidFileExtensionError(Exception):
    pass

class FileSizeExceededError(Exception):
    pass


class File:
    ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls'}
    FILE_SIZE = 10 * 1024 * 1024 # 10 mb

    def __init__(self, filename: str, content: bytes, mime_type: str, description: str):
        self._filename = filename
        self._content = content
        self._mime_type = mime_type
        self._description = description

        # 2. Validamos el estado interno
        self._validate()

    # "Getters" (Properties), encapsulamiento de atributos
    @property
    def filename(self) -> str:
        return self._filename

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def mime_type(self) -> str:
        return self._mime_type

    @property
    def description(self) -> str:
        return self._description

    def _validate(self):
        _, ext = os.path.splitext(self._filename)

        if len(self._content) > self.FILE_SIZE:
            raise FileSizeExceededError("El archivo excede el tamaño permitido.")

        if ext.lower() not in self.ALLOWED_EXTENSIONS:
            raise InvalidFileExtensionError("Solo se permiten archivos CSV y XLSX.")

class StorageInterface(ABC):

    @abstractmethod
    def upload(self, file: File) -> str:
        pass