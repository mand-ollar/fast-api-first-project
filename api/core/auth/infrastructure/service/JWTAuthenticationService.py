import os
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from ulid import ULID

from core.auth.domain.entity import Principal
from core.auth.domain.enum import CredentialType
from core.auth.domain.exception import InvalidCredentials, InvalidPrincipal
from core.auth.domain.repository import CredentialsRepository, PrincipalRepository
from core.auth.domain.service import AuthenticationService, PasswordHasher
from core.auth.domain.valueobject import Credentials

SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY", "TEST_KEY")
ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("AUTH_TOKEN_LIFE_DAY", "1825"))  # 5 years
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("AUTH_TOKEN_LIFE_DAY", "1825"))  # 5 years


class JWTAuthenticationService(AuthenticationService):
    def __init__(
        self,
        password_hasher: PasswordHasher,
        principal_repo: PrincipalRepository,
        credentials_repo: CredentialsRepository,
        secret_key: str = SECRET_KEY,
        short_days: int = ACCESS_TOKEN_EXPIRE_DAYS,
        long_days: int = REFRESH_TOKEN_EXPIRE_DAYS,
    ) -> None:
        self.password_hasher: PasswordHasher = password_hasher
        self.principal_repo: PrincipalRepository = principal_repo
        self.credentials_repo: CredentialsRepository = credentials_repo
        self.secret_key: str = secret_key
        self.short_delta: timedelta = timedelta(days=short_days)
        self.long_delta: timedelta = timedelta(days=long_days)

    def authenticate(self, principal_str: str, secret: str) -> tuple[Credentials, Credentials]:
        # load and verify principal
        principal: Principal = self.principal_repo.get_by_principal(principal=principal_str)
        if not principal:
            raise InvalidPrincipal("Invalid principal")
        if not principal.verify_password(plain=secret, hasher=self.password_hasher):
            raise InvalidCredentials("Invalid secret")

        now: datetime = datetime.now(tz=timezone.utc)
        issued_at: int = int(now.timestamp())

        # issue short-lived credentials
        jwt_token_id_short: ULID = ULID()
        expiration_time_short: int = int((now + self.short_delta).timestamp())
        payload_short: dict[str, Any] = {
            "sub": str(principal.user_id),
            "iat": issued_at,
            "exp": expiration_time_short,
            "jti": str(jwt_token_id_short),
            "token_type": CredentialType.SHORT_LIVED.value,
            "role": principal.role.value,
        }
        raw_short: str = jwt.encode(payload_short, key=self.secret_key, algorithm="HS256")
        short_creds: Credentials = Credentials(
            user_id=principal.user_id, type=CredentialType.SHORT_LIVED, raw_value=raw_short
        )

        # issue long-lived credentials
        jwt_token_id_long: ULID = ULID()
        expiration_time_long: int = int((now + self.long_delta).timestamp())
        payload_long: dict[str, Any] = {
            "sub": str(principal.user_id),
            "iat": issued_at,
            "exp": expiration_time_long,
            "jti": str(jwt_token_id_long),
            "token_type": CredentialType.LONG_LIVED.value,
            "role": principal.role.value,
        }
        raw_long: str = jwt.encode(payload_long, key=self.secret_key, algorithm="HS256")
        long_creds: Credentials = Credentials(
            user_id=principal.user_id, type=CredentialType.LONG_LIVED, raw_value=raw_long
        )

        # persist both credentials
        self.credentials_repo.save(creds=short_creds)
        self.credentials_repo.save(creds=long_creds)

        return short_creds, long_creds

    def refresh(self, raw_long_lived_credential: str) -> tuple[Credentials, Credentials]:
        # decode & validate old token
        data: dict[str, Any] = jwt.decode(raw_long_lived_credential, key=self.secret_key, algorithms=["HS256"])
        if data.get("token_type") != CredentialType.LONG_LIVED.value:
            raise InvalidCredentials("Expected a long-lived credential for refresh")

        # check stored credentials
        refresh_creds: Credentials = Credentials(
            user_id=ULID.from_str(data["sub"]),
            type=CredentialType.LONG_LIVED,
            raw_value=raw_long_lived_credential,
        )
        if not self.credentials_repo.exists(creds=refresh_creds):
            raise InvalidCredentials("Refresh credential revoked or unknown")

        # revoke old refresh
        self.credentials_repo.revoke(creds=refresh_creds)

        now: datetime = datetime.now(tz=timezone.utc)
        issued_at: int = int(now.timestamp())

        # new short-lived
        jwt_token_id_short: ULID = ULID()
        expiration_time_short: int = int((now + self.short_delta).timestamp())
        payload_short: dict[str, Any] = {
            "sub": str(refresh_creds.user_id),
            "iat": issued_at,
            "exp": expiration_time_short,
            "jti": str(jwt_token_id_short),
            "token_type": CredentialType.SHORT_LIVED.value,
            "role": data["role"],
        }
        raw_short: str = jwt.encode(payload_short, self.secret_key, algorithm="HS256")
        new_short: Credentials = Credentials(
            user_id=refresh_creds.user_id, type=CredentialType.SHORT_LIVED, raw_value=raw_short
        )

        # new long-lived
        jwt_token_id_long: ULID = ULID()
        expiration_time_long: int = int((now + self.long_delta).timestamp())
        payload_long: dict[str, Any] = {
            "sub": str(refresh_creds.user_id),
            "iat": issued_at,
            "exp": expiration_time_long,
            "jti": str(jwt_token_id_long),
            "token_type": CredentialType.LONG_LIVED.value,
            "role": data["role"],
        }
        raw_long: str = jwt.encode(payload_long, self.secret_key, algorithm="HS256")
        new_long: Credentials = Credentials(
            user_id=refresh_creds.user_id, type=CredentialType.LONG_LIVED, raw_value=raw_long
        )

        # persist new credentials
        self.credentials_repo.save(creds=new_short)
        self.credentials_repo.save(creds=new_long)

        return new_short, new_long

    def verify(self, raw_short_lived_credential: str) -> ULID:
        data: dict[str, Any] = jwt.decode(raw_short_lived_credential, key=self.secret_key, algorithms=["HS256"])
        creds: Credentials = Credentials(
            user_id=ULID.from_str(data["sub"]),
            type=CredentialType.SHORT_LIVED,
            raw_value=raw_short_lived_credential,
        )
        if not self.credentials_repo.exists(creds=creds):
            raise InvalidCredentials("Access credential revoked or unknown")
        return creds.user_id

    def revoke(self, raw_token: str) -> None:
        # Decode to figure out type and user_id
        data: dict[str, Any] = jwt.decode(raw_token, key=self.secret_key, algorithms=["HS256"])
        creds: Credentials = Credentials(
            user_id=ULID.from_str(data["sub"]),
            type=CredentialType(data["token_type"]),
            raw_value=raw_token,
        )
        self.credentials_repo.revoke(creds=creds)
