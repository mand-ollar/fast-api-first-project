from enum import Enum


class CredentialType(str, Enum):
    SHORT_LIVED = "SHORT_LIVED"
    LONG_LIVED = "LONG_LIVED"
