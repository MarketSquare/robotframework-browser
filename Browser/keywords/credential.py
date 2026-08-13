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

        The credential is created in the currently active context and it is used by all
        pages that are created from that context. There must be an open context, otherwise
        the keyword fails.

        | =Arguments= | =Description= |
        | rpId | Relying party id (typically the site's effective domain). |
        | id_ | Base64url-encoded credential id. Auto-generated if omitted. |
        | privateKey | Base64url-encoded PKCS#8 (DER) private key. Auto-generated if omitted. |
        | publicKey | Base64url-encoded SPKI (DER) public key. Auto-generated if omitted. |
        | userHandle | Base64url-encoded user handle. Auto-generated if omitted. |

        Because ``privateKey`` and ``publicKey`` are sensitive information, it is recommended
        to wrap their values in the Secret type. The Secret type requires Robot Framework 7.4
        or newer. If you are using Robot Framework 7.3 or older, the keyword supports resolving
        ``privateKey`` and ``publicKey`` from Robot Framework variables and environment
        variables in the following ways. The keyword resolves the value from a Robot Framework
        variable internally, when the variable is prefixed with ``$``, without the curly
        braces. Example: ``$publicKey`` will resolve to the ``${publicKey}`` Robot Framework
        variable.

        If the ``privateKey`` or ``publicKey`` value is prefixed with ``%``, the library will
        resolve the corresponding environment variable. Example: ``%PUBLICKEY`` will
        resolve to the ``%{PUBLICKEY}`` environment variable.

        Plain values are not accepted. If the given ``privateKey`` or ``publicKey`` is not a
        Secret and does not resolve to another value, the keyword fails with an error stating
        that direct assignment of values or variables is not allowed.

        Example:
        | `New Context`
        | ${credentials} =    Get Credentials   # This is a helper keyword that returns a dictionary with the required credential parameters.
        | `Create Credential`
        | ...    rpId=${DOMAIN_NAME}
        | ...    id_=${credentials["id"]}
        | ...    privateKey=${credentials["privateKey"]}    # This should be a Secret type or a string starting with $ which resolves to a Robot Framework variable.
        | ...    publicKey=${credentials["publicKey"]}    # This should be a Secret type or a string starting with $ which resolves to a Robot Framework variable.
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

        Overrides ``navigator.credentials.create()`` and ``navigator.credentials.get()``
        in all current and future pages of the context. Call this before the page first
        touches ``navigator.credentials``.

        Until the authenticator is installed, no interception is in place and the page sees
        the platform's native (or absent) WebAuthn behavior. `Create Credential` installs
        the authenticator as well, so this keyword is mainly needed when the credentials are
        created by the application itself. There must be an open context, otherwise the
        keyword fails.

        Example:
        | `New Context`
        | `Install Credential`
        | `New Page`    ${SUT_URL}
        | # Do something on the page that causes the page to call ``navigator.credentials.create()``
        | ${credential_id} =    Get Credential Id   # This is a user keyword that returns the credential id from somewhere. Talk to your application team to find out how to get the credential id.
        | ${credential} =    `Get Credential`    id_=${credential_id}    # This will return the credential that was created by the application and installed into the context.
        | `New Context`
        | `Create Credential`
        | ...    rpId=${DOMAIN_NAME}
        | ...    id_=${credential["id"]}
        | ...    privateKey=${credential["privateKey"]}
        | ...    publicKey=${credential["publicKey"]}
        | ...    userHandle=${credential["userHandle"]}
        | `New Page`    ${SUT_URL}
        | # User should be able to interact with the page using the installed credential.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.InstallCredential(Request.Empty())
        logger.info(f"Credential installed with response: {response.log}")

    @keyword(tags=("Getter", "Credential"))
    def get_credential(
        self, id_: str | None = None, rpId: str | None = None
    ) -> ClientCredential:
        """Returns the credential matching the given id and/or rpId.

        At least one of ``id_`` and ``rpId`` must be given, otherwise the keyword fails.
        If both are given, the credential must match both of them. When more than one
        credential matches, the first match is returned. When no credential matches, the
        keyword fails.

        | =Arguments= | =Description= |
        | id_ | Base64url-encoded credential id. |
        | rpId | Relying party id (typically the site's effective domain). |

        The returned credential is a dictionary with the following keys:
        | =Key= | =Description= |
        | id | Base64url-encoded credential id. |
        | rpId | Relying party id (typically the site's effective domain). |
        | userHandle | Base64url-encoded user handle. |
        | privateKey | Base64url-encoded PKCS#8 (DER) private key as a Secret. |
        | publicKey | Base64url-encoded SPKI (DER) public key as a Secret. |

        The privateKey and publicKey are wrapped in the
        [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#secret-variables|Secret]
        type, so that their values are not shown in the Robot Framework log. The values
        themselves are available in the ``value`` attribute. Note that the node side of the
        library might write the whole credential, including the private key, as plain text to the
        playwright-log.txt file. See `PlaywrightLogTypes` for how to control that file.

        See `Install Credential` for more information about how to use
        this keyword.

        Example:
        | ${credential} =    `Get Credential`    id_=${CREDENTIAL_ID}
        | Should Be Equal    ${credential["id"]}    ${CREDENTIAL_ID}
        | Should Be Equal    ${credential["rpId"]}    ${DOMAIN_NAME}
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

        Deleting a credential which does not exist does not fail. There must be an open
        context, otherwise the keyword fails.

        Example:
        | `Delete Credential`    id_=${CREDENTIAL_ID}
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.DeleteCredential(
                Request.CredentialIdAndRpId(id=id_, rpId=ROBOT_FRAMEWORK_BROWSER_NO_SET)
            )
        logger.info(f"Deleted credential with response: {response.log}")
