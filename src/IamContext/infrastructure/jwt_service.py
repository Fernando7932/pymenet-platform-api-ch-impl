import os
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv(override=True)


class JWTService:
    """
    Servicio de infraestructura para generar y verificar JSON Web Tokens.
    Este servicio NO pertenece al dominio, es un detalle técnico de autenticación.
    """

    def __init__(self):
        self._secret = os.getenv('JWT_SECRET')
        if not self._secret:
            raise ValueError("JWT_SECRET no está configurado en las variables de entorno.")
        self._algorithm = 'HS256'
        self._expiration_hours = 24

    def generate_token(self, user_data: dict) -> str:
        """
        Genera un JWT firmado con los datos del usuario.
        El token expira en 24 horas.
        """
        payload = {
            **user_data,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=self._expiration_hours),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def verify_token(self, token: str) -> dict:
        """
        Decodifica y valida un JWT.
        Lanza jwt.ExpiredSignatureError si expiró.
        Lanza jwt.InvalidTokenError si es inválido.
        """
        return jwt.decode(token, self._secret, algorithms=[self._algorithm])
