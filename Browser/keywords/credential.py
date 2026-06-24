# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import ROBOT_FRAMEWORK_BROWSER_NO_SET, ClientCredential, keyword, logger
from ..utils.types import Secret


class Credential(LibraryComponent):
    @keyword(tags=("Setter", "Credential"))
    def create_credential(
        self,
        rpId: str,
        id_: str | None = None,
        privateKey: Secret | str | None = None,
        publicKey: Secret | str | None = None,
        userHandle: str | None = None,
    ):
        """Creates a credential with the given parameters.

        Will always [create|https://playwright.dev/docs/api/class-credentials#credentials-create]
        and [install|https://playwright.dev/docs/api/class-credentials#credentials-install] the
        credential, even if the optional parameters are not provided. In this case Playwright will
        autogenerate the missing values.

        Create credential is set to the context and will be used for all subsequent pages that
        are created from the context.

        | =Arguments= | =Description= |
        | rpId | Relying party id (typically the site's effective domain). |
        | id_ | Base64url-encoded credential id. Auto-generated if omitted. |
        | privateKey | Base64url-encoded PKCS#8 (DER) private key. Auto-generated if omitted. |
        | publicKey | Base64url-encoded SPKI (DER) public key. Auto-generated if omitted. |
        | userHandle | Base64url-encoded user handle. Auto-generated if omitted. |

        Because privateKey and publicKey are sensitive information, it recommended to privateKey
        and publicKey wrapped in the Secret type. If you using Robot Framework 7.3 or older,
        then keyword support resolving privateKey and publicKey from environment variables and
        Robot Framework variables in the following ways. Keyword resolves the ``privateKey``
        and ``publicKey`` from Robot Framework variable internally, when variable is prefixed
        with `$`, without the curly braces. Example `$publicKey`` will resolve to
        ``${publicKey}`` Robot Framework variable.

        If ``privateKey`` and ``publicKey`` variable is prefixed with `%`, library will resolve
        corresponding environment variable. Example ``%PUBLICKEY`` will
        resolve to ``%{PUBLICKEY}`` environment variable.

        Example:
        | ${credentials} =    Get Credentials   # This is a helper keyword that returns a dictionary with the required credential parameters.
        | `Create Credential`
        | ...    rpId=localhost
        | ...    id_=${credentials["id"]}
        | ...    privateKey=${credentials["privateKey"]}
        | ...    publicKey=${credentials["publicKey"]}
        | ...    userHandle=${credentials["userHandle"]}
        | `New Page`    ${SUT_URL}
        | `Click`    id=login
        | `Get Text`    id=status    ==    Success
        """
        logger.info(f"Creating credential with rpId: {rpId}, id: {id_}")
        cred_id = id_ if id_ is not None else ROBOT_FRAMEWORK_BROWSER_NO_SET
        if privateKey is None:
            priv_key = ROBOT_FRAMEWORK_BROWSER_NO_SET
        else:
            priv_key = self.resolve_secret(privateKey, "privateKey")
        if publicKey is None:
            pub_key = ROBOT_FRAMEWORK_BROWSER_NO_SET
        else:
            pub_key = self.resolve_secret(publicKey, "publicKey")
        user_handle = (
            userHandle if userHandle is not None else ROBOT_FRAMEWORK_BROWSER_NO_SET
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.CreateCredential(
                Request.CreateCredential(
                    rpId=rpId,
                    id=cred_id,
                    privateKey=priv_key,
                    publicKey=pub_key,
                    userHandle=user_handle,
                )
            )
        logger.info(f"Credential created with response: {response.log}")

    @keyword(tags=("Setter", "Credential"))
    def install_credential(self):
        """Installs the virtual WebAuthn authenticator into the context.

        Overriding `navigator.credentials.create()` and `navigator.credentials.get()`
        in all current and future pages. Call this before the page first touches
        `navigator.credentials`.

        Required: until `credentials.install()` is called, no interception is in place
        and the page sees the platform's native (or absent) WebAuthn behavior. Seeding
        credentials with `credentials.create()` without installing populates the
        authenticator, but the page will never see those credentials.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.InstallCredential(Request.Empty())
        logger.info(f"Credential installed with response: {response.log}")

    @keyword(tags=("Getter", "Credential"))
    def get_credential(
        self, id_: str | None = None, rpId: str | None = None
    ) -> ClientCredential:
        """Returns the credential with the given id.

        | =Arguments= | =Description= |
        | id_ | Base64url-encoded credential id. |
        | rpId | Relying party id (typically the site's effective domain). |

        The returned credential is a dictionary with the following keys:
        | =Key= | =Description= |
        | id | Base64url-encoded credential id. |
        | rpId | Relying party id (typically the site's effective domain). |
        | privateKey | Base64url-encoded PKCS#8 (DER) private key
        | publicKey | Base64url-encoded SPKI (DER) public key |

        The privateKey and publicKey are wrapped in the
        [Secret|https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#secret-variables]
        type, to prevent accidental logging of sensitive information.

        Example:
        | ${credential} =    Get Credential    id=localhost
        | Should Be Equal    ${credential["id"]}    localhost
        | Should Be Equal    ${credential["rpId"]}    localhost
        | Should Be Equal    ${credential["userHandle"]}    userhandleCreatedByTheApp
        | Should Be Equal    ${credential["privateKey"].value}    privateKeyCreatedByTheApp
        | Should Be Equal    ${credential["publicKey"].value}    publicKeyCreatedByTheApp
        """
        if not id_ and not rpId:
            raise ValueError("Either id_ or rpId must be provided.")
        cred_id = id_ if id_ is not None else ROBOT_FRAMEWORK_BROWSER_NO_SET
        cred_rpId = rpId if rpId is not None else ROBOT_FRAMEWORK_BROWSER_NO_SET
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCredential(
                Request.CredentialIdAndRpId(id=cred_id, rpId=cred_rpId)
            )
        logger.info(f"Retrieved credential with response: {response.log}")
        logger.info(
            f"Retrieved credential with id: {response.id}, rpId: {response.rpId}"
        )
        return {
            "id": response.id,
            "rpId": response.rpId,
            "privateKey": Secret(response.privateKey),
            "publicKey": Secret(response.publicKey),
            "userHandle": response.userHandle,
        }

    @keyword(tags=("Setter", "Credential"))
    def delete_credential(self, id_: str):
        """Deletes the credential with the given id.

        | =Arguments= | =Description= |
        | id_ | Base64url-encoded credential id. |

        Example:
        | `Delete Credential`    id=localhost
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.DeleteCredential(
                Request.CredentialIdAndRpId(id=id_, rpId=ROBOT_FRAMEWORK_BROWSER_NO_SET)
            )
        logger.info(f"Deleted credential with response: {response.log}")
