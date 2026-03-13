from passlib.context import CryptContext


class BcryptPasswordHasher:
    def __init__(self, context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")) -> None:
        self.context: CryptContext = context

    def hash(self, secret: str) -> str:
        return self.context.hash(secret=secret)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.context.verify(secret=plain, hash=hashed)
