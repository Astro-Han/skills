from .model import Credential


def rotate(credential: Credential, token: str) -> None:
    credential.token = token
