from typing import TypedDict

from Browser.utils.types import Secret


class Credentials(TypedDict):
    id: str
    privateKey: Secret
    publicKey: Secret
    userHandle: str


def get_credentials() -> Credentials:
    return {
        "id": "1mXB1BEvCEDjdteOXO-xUQ",
        "privateKey": Secret("MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgoU1hcxESzMuQ20KpmLchY7JAF5vjna6XrCMaLXvuzGKhRANCAATS8XYWc35KTNo_lueg8qxDMJFMeIi8fjSXWOtlcGdh2zJLM0n3Sv3gPSq1zhB8oOFRwugGRhffM1XrwOlDoQ4R"),
        "publicKey": Secret("MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE0vF2FnN-SkzaP5bnoPKsQzCRTHiIvH40l1jrZXBnYdsySzNJ90r94D0qtc4QfKDhUcLoBkYX3zNV68DpQ6EOEQ"),
        "userHandle": "aGFyZGNvZGVkLXVzZXItaGFuZGxl"
    }
