from .model import Credential


def rotate_row(credential: Credential, row: dict[str, str]) -> None:
    credential.token = row["token"]
