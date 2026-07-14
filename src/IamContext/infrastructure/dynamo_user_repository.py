import os
import boto3
from dotenv import load_dotenv
from src.IamContext.domain.interfaces import UserRepositoryInterface
from src.IamContext.domain.entities import Usuario
from src.IamContext.domain.value_objects import (
    UsuarioId, Email, EstadoUsuario, CredencialesUsuario
)

load_dotenv(override=True)


class DynamoUserRepository(UserRepositoryInterface):
    """Implementación concreta del repositorio de usuarios usando DynamoDB"""

    def __init__(self):
        self._table_name = os.getenv('USERS_TABLE_NAME', 'pymenet-users-dev')

        # En Lambda, boto3 se conecta automáticamente con el rol de IAM
        # En local, usa las credenciales de ~/.aws/credentials o env vars
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self._table = dynamodb.Table(self._table_name)

    def find_by_email(self, email: str) -> Usuario | None:
        """Busca un usuario por su email (Partition Key de DynamoDB)"""
        response = self._table.get_item(Key={'email': email.strip().lower()})

        item = response.get('Item')
        if item is None:
            return None

        # Reconstruir el Aggregate Root desde los datos persistidos
        return Usuario(
            id=UsuarioId(item['user_id']),
            nombre=item['nombre'],
            email=Email(item['email']),
            credenciales=CredencialesUsuario(item['password_hash']),
            estado=EstadoUsuario(item['estado'])
        )

    def save(self, usuario: Usuario) -> None:
        """Persiste un usuario nuevo en DynamoDB"""
        self._table.put_item(Item={
            'email': usuario.email.direccion,           # Partition Key
            'user_id': usuario.id.value,
            'nombre': usuario.nombre,
            'password_hash': usuario.credenciales.hash_contrasena,
            'estado': usuario.estado.value
        })