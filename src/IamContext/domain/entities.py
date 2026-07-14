from src.IamContext.domain.value_objects import (
    UsuarioId, Email, EstadoUsuario, CredencialesUsuario,
    UsuarioBloqueadoError, CredencialesInvalidasError
)
import bcrypt


class Usuario:
    """
    Aggregate Root del Bounded Context IAM.
    Representa un usuario del sistema con su identidad, credenciales y estado.
    """

    def _init_(self, id: UsuarioId, nombre: str, email: Email,
                 credenciales: CredencialesUsuario, estado: EstadoUsuario):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._credenciales = credenciales
        self._estado = estado

    @property
    def id(self) -> UsuarioId:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> Email:
        return self._email

    @property
    def credenciales(self) -> CredencialesUsuario:
        return self._credenciales

    @property
    def estado(self) -> EstadoUsuario:
        return self._estado


    def iniciar_sesion(self, plain_password: str) -> bool:
        """
        Método de dominio: valida que el usuario pueda iniciar sesión.
        Verifica el estado y las credenciales.
        """
        if self._estado != EstadoUsuario.ACTIVO:
            raise UsuarioBloqueadoError("El usuario se encuentra bloqueado.")

        password_bytes = plain_password.encode('utf-8')
        hash_bytes = self._credenciales.hash_contrasena.encode('utf-8')

        if not bcrypt.checkpw(password_bytes, hash_bytes):
            raise CredencialesInvalidasError("Las credenciales son incorrectas.")

        return True


    @staticmethod
    def registrar(id_value: str, nombre: str, email_str: str, plain_password: str) -> 'Usuario':
        """
        Factory Method: crea un Usuario nuevo con contraseña hasheada.
        Centraliza la lógica de creación para garantizar un estado válido.
        """
        usuario_id = UsuarioId(id_value)
        email = Email(email_str)

        # Hashear la contraseña con bcrypt (salt automático)
        password_bytes = plain_password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        credenciales = CredencialesUsuario(hashed.decode('utf-8'))

        estado = EstadoUsuario.ACTIVO

        return Usuario(usuario_id, nombre, email, credenciales, estado)