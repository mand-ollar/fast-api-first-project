from core.auth.domain.enum import CredentialType
from core.auth.domain.exception import InvalidCredentials
from core.auth.domain.valueobject import Credentials
from core.auth.infrastructure.repository.credentials.entity import CredentialsAlchemyEntity


class CredentialsMapper:
    @staticmethod
    def to_alchemy_entity(domain_entity: Credentials) -> CredentialsAlchemyEntity:
        if domain_entity.type == CredentialType.SHORT_LIVED:
            return CredentialsAlchemyEntity(
                user_id=str(domain_entity.user_id),
                access_key=domain_entity.raw_value,
            )
        elif domain_entity.type == CredentialType.LONG_LIVED:
            return CredentialsAlchemyEntity(
                user_id=str(domain_entity.user_id),
                refresh_key=domain_entity.raw_value,
            )
        else:
            raise InvalidCredentials("Invalid credentials type")
