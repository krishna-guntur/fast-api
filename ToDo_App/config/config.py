from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'ab09b68154f8cece068a572a482cfe0dbe3a8fc1128bc768f9c8291a61ebf8d3'
ALGORITHM = 'HS256'
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')