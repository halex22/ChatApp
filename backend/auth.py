from datetime import datetime, timedelta, timezone
from os import getenv

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = 'HS256'


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


if __name__ == '__main__':
    a = {'a': 12}
    print(a)
    b = a.copy()

    print(a)
    # print(b)
