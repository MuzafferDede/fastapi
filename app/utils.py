from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return pwd_context.hash(password)

def verify(password, hashed) -> bool:
    return pwd_context.verify(password, hashed)

