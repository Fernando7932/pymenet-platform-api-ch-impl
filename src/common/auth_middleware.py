import os
import jwt
from dotenv import load_dotenv

load_dotenv(override=True)


def verify_jwt_token(event: dict) -> dict:
    """
    Middleware compartido: extrae y valida el JWT del header Authorization.
    Retorna los datos del usuario si el token es válido.
    Lanza una excepción si el token es inválido o no existe.
    """
    headers = event.get('headers', {})

    # API Gateway puede enviar los headers en minúsculas o con capitalización
    auth_header = headers.get('Authorization') or headers.get('authorization')

    if not auth_header:
        raise PermissionError("Token de autenticación no proporcionado.")

    # Formato esperado: "Bearer eyJhbG..."
    parts = auth_header.split(' ')
    if len(parts) != 2 or parts[0] != 'Bearer':
        raise PermissionError("Formato de token inválido. Use: Bearer <token>")

    token = parts[1]
    secret = os.getenv('JWT_SECRET')

    if not secret:
        raise ValueError("JWT_SECRET no está configurado.")

    try:
        decoded = jwt.decode(token, secret, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        raise PermissionError("El token ha expirado. Inicie sesión nuevamente.")
    except jwt.InvalidTokenError:
        raise PermissionError("Token de autenticación inválido.")
