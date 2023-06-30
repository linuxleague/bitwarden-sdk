from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, Union, TypeVar, Type, Callable, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class DeviceType(Enum):
    """Device type to send to Bitwarden. Defaults to SDK"""
    ANDROID = "Android"
    ANDROID_AMAZON = "AndroidAmazon"
    CHROME_BROWSER = "ChromeBrowser"
    CHROME_EXTENSION = "ChromeExtension"
    EDGE_BROWSER = "EdgeBrowser"
    EDGE_EXTENSION = "EdgeExtension"
    FIREFOX_BROWSER = "FirefoxBrowser"
    FIREFOX_EXTENSION = "FirefoxExtension"
    IE_BROWSER = "IEBrowser"
    I_OS = "iOS"
    LINUX_DESKTOP = "LinuxDesktop"
    MAC_OS_DESKTOP = "MacOsDesktop"
    OPERA_BROWSER = "OperaBrowser"
    OPERA_EXTENSION = "OperaExtension"
    SAFARI_BROWSER = "SafariBrowser"
    SAFARI_EXTENSION = "SafariExtension"
    SDK = "SDK"
    UNKNOWN_BROWSER = "UnknownBrowser"
    UWP = "UWP"
    VIVALDI_BROWSER = "VivaldiBrowser"
    VIVALDI_EXTENSION = "VivaldiExtension"
    WINDOWS_DESKTOP = "WindowsDesktop"


@dataclass
class ClientSettings:
    """Basic client behavior settings. These settings specify the various targets and behavior
    of the Bitwarden Client. They are optional and uneditable once the client is
    initialized.
    
    Defaults to
    
    ``` # use bitwarden::client::client_settings::{ClientSettings, DeviceType}; # use
    assert_matches::assert_matches; let settings = ClientSettings { identity_url:
    "https://identity.bitwarden.com".to_string(), api_url:
    "https://api.bitwarden.com".to_string(), user_agent: "Bitwarden Rust-SDK".to_string(),
    device_type: DeviceType::SDK, }; let default = ClientSettings::default();
    assert_matches!(settings, default); ```
    
    Targets `localhost:8080` for debug builds.
    """
    """The api url of the targeted Bitwarden instance. Defaults to `https://api.bitwarden.com`"""
    api_url: str
    """Device type to send to Bitwarden. Defaults to SDK"""
    device_type: DeviceType
    """The identity url of the targeted Bitwarden instance. Defaults to
    `https://identity.bitwarden.com`
    """
    identity_url: str
    """The user_agent to sent to Bitwarden. Defaults to `Bitwarden Rust-SDK`"""
    user_agent: str

    @staticmethod
    def from_dict(obj: Any) -> 'ClientSettings':
        assert isinstance(obj, dict)
        api_url = from_str(obj.get("apiUrl"))
        device_type = DeviceType(obj.get("deviceType"))
        identity_url = from_str(obj.get("identityUrl"))
        user_agent = from_str(obj.get("userAgent"))
        return ClientSettings(api_url, device_type, identity_url, user_agent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["apiUrl"] = from_str(self.api_url)
        result["deviceType"] = to_enum(DeviceType, self.device_type)
        result["identityUrl"] = from_str(self.identity_url)
        result["userAgent"] = from_str(self.user_agent)
        return result


@dataclass
class AccessTokenLoginRequest:
    """Login to Bitwarden with access token"""
    """Bitwarden service API access token"""
    access_token: str

    @staticmethod
    def from_dict(obj: Any) -> 'AccessTokenLoginRequest':
        assert isinstance(obj, dict)
        access_token = from_str(obj.get("accessToken"))
        return AccessTokenLoginRequest(access_token)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accessToken"] = from_str(self.access_token)
        return result


@dataclass
class APIKeyLoginRequest:
    """Login to Bitwarden with Api Key"""
    """Bitwarden account client_id"""
    client_id: str
    """Bitwarden account client_secret"""
    client_secret: str
    """Bitwarden account master password"""
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'APIKeyLoginRequest':
        assert isinstance(obj, dict)
        client_id = from_str(obj.get("clientId"))
        client_secret = from_str(obj.get("clientSecret"))
        password = from_str(obj.get("password"))
        return APIKeyLoginRequest(client_id, client_secret, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["clientId"] = from_str(self.client_id)
        result["clientSecret"] = from_str(self.client_secret)
        result["password"] = from_str(self.password)
        return result


@dataclass
class FingerprintRequest:
    """The input material, used in the fingerprint generation process."""
    fingerprint_material: str
    """The user's public key"""
    public_key: str

    @staticmethod
    def from_dict(obj: Any) -> 'FingerprintRequest':
        assert isinstance(obj, dict)
        fingerprint_material = from_str(obj.get("fingerprintMaterial"))
        public_key = from_str(obj.get("publicKey"))
        return FingerprintRequest(fingerprint_material, public_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fingerprintMaterial"] = from_str(self.fingerprint_material)
        result["publicKey"] = from_str(self.public_key)
        return result


@dataclass
class SecretVerificationRequest:
    """The user's master password to use for user verification. If supplied, this will be used
    for verification purposes.
    """
    master_password: Optional[str] = None
    """Alternate user verification method through OTP. This is provided for users who have no
    master password due to use of Customer Managed Encryption. Must be present and valid if
    master_password is absent.
    """
    otp: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SecretVerificationRequest':
        assert isinstance(obj, dict)
        master_password = from_union([from_none, from_str], obj.get("masterPassword"))
        otp = from_union([from_none, from_str], obj.get("otp"))
        return SecretVerificationRequest(master_password, otp)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.master_password is not None:
            result["masterPassword"] = from_union([from_none, from_str], self.master_password)
        if self.otp is not None:
            result["otp"] = from_union([from_none, from_str], self.otp)
        return result


@dataclass
class PasswordLoginRequest:
    """Login to Bitwarden with Username and Password"""
    """Bitwarden account email address"""
    email: str
    """Bitwarden account master password"""
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'PasswordLoginRequest':
        assert isinstance(obj, dict)
        email = from_str(obj.get("email"))
        password = from_str(obj.get("password"))
        return PasswordLoginRequest(email, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_str(self.email)
        result["password"] = from_str(self.password)
        return result


@dataclass
class ProjectCreateRequest:
    name: str
    """Organization where the project will be created"""
    organization_id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'ProjectCreateRequest':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        organization_id = UUID(obj.get("organizationId"))
        return ProjectCreateRequest(name, organization_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["organizationId"] = str(self.organization_id)
        return result


@dataclass
class ProjectsDeleteRequest:
    """IDs of the projects to delete"""
    ids: List[UUID]

    @staticmethod
    def from_dict(obj: Any) -> 'ProjectsDeleteRequest':
        assert isinstance(obj, dict)
        ids = from_list(lambda x: UUID(x), obj.get("ids"))
        return ProjectsDeleteRequest(ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ids"] = from_list(lambda x: str(x), self.ids)
        return result


@dataclass
class ProjectGetRequest:
    """ID of the project to retrieve"""
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'ProjectGetRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return ProjectGetRequest(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class ProjectsListRequest:
    """Organization to retrieve all the projects from"""
    organization_id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'ProjectsListRequest':
        assert isinstance(obj, dict)
        organization_id = UUID(obj.get("organizationId"))
        return ProjectsListRequest(organization_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["organizationId"] = str(self.organization_id)
        return result


@dataclass
class ProjectPutRequest:
    """ID of the project to modify"""
    id: UUID
    name: str
    """Organization ID of the project to modify"""
    organization_id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'ProjectPutRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        organization_id = UUID(obj.get("organizationId"))
        return ProjectPutRequest(id, name, organization_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        result["organizationId"] = str(self.organization_id)
        return result


@dataclass
class ProjectsCommand:
    """> Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Retrieve a project by the provided identifier
    
    Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Creates a new project in the provided organization using the given data
    
    Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Lists all projects of the given organization
    
    Returns: [ProjectsResponse](crate::sdk::response::projects_response::ProjectsResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Updates an existing project with the provided ID using the given data
    
    Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Deletes all the projects whose IDs match the provided ones
    
    Returns:
    [ProjectsDeleteResponse](crate::sdk::response::projects_response::ProjectsDeleteResponse)
    """
    get: Optional[ProjectGetRequest] = None
    create: Optional[ProjectCreateRequest] = None
    list: Optional[ProjectsListRequest] = None
    update: Optional[ProjectPutRequest] = None
    delete: Optional[ProjectsDeleteRequest] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ProjectsCommand':
        assert isinstance(obj, dict)
        get = from_union([ProjectGetRequest.from_dict, from_none], obj.get("get"))
        create = from_union([ProjectCreateRequest.from_dict, from_none], obj.get("create"))
        list = from_union([ProjectsListRequest.from_dict, from_none], obj.get("list"))
        update = from_union([ProjectPutRequest.from_dict, from_none], obj.get("update"))
        delete = from_union([ProjectsDeleteRequest.from_dict, from_none], obj.get("delete"))
        return ProjectsCommand(get, create, list, update, delete)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.get is not None:
            result["get"] = from_union([lambda x: to_class(ProjectGetRequest, x), from_none], self.get)
        if self.create is not None:
            result["create"] = from_union([lambda x: to_class(ProjectCreateRequest, x), from_none], self.create)
        if self.list is not None:
            result["list"] = from_union([lambda x: to_class(ProjectsListRequest, x), from_none], self.list)
        if self.update is not None:
            result["update"] = from_union([lambda x: to_class(ProjectPutRequest, x), from_none], self.update)
        if self.delete is not None:
            result["delete"] = from_union([lambda x: to_class(ProjectsDeleteRequest, x), from_none], self.delete)
        return result


@dataclass
class SecretCreateRequest:
    key: str
    note: str
    """Organization where the secret will be created"""
    organization_id: UUID
    value: str
    """IDs of the projects that this secret will belong to"""
    project_ids: Optional[List[UUID]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SecretCreateRequest':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        note = from_str(obj.get("note"))
        organization_id = UUID(obj.get("organizationId"))
        value = from_str(obj.get("value"))
        project_ids = from_union([from_none, lambda x: from_list(lambda x: UUID(x), x)], obj.get("projectIds"))
        return SecretCreateRequest(key, note, organization_id, value, project_ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["note"] = from_str(self.note)
        result["organizationId"] = str(self.organization_id)
        result["value"] = from_str(self.value)
        if self.project_ids is not None:
            result["projectIds"] = from_union([from_none, lambda x: from_list(lambda x: str(x), x)], self.project_ids)
        return result


@dataclass
class SecretsDeleteRequest:
    """IDs of the secrets to delete"""
    ids: List[UUID]

    @staticmethod
    def from_dict(obj: Any) -> 'SecretsDeleteRequest':
        assert isinstance(obj, dict)
        ids = from_list(lambda x: UUID(x), obj.get("ids"))
        return SecretsDeleteRequest(ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ids"] = from_list(lambda x: str(x), self.ids)
        return result


@dataclass
class SecretGetRequest:
    """ID of the secret to retrieve"""
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'SecretGetRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return SecretGetRequest(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class SecretIdentifiersRequest:
    """Organization to retrieve all the secrets from"""
    organization_id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'SecretIdentifiersRequest':
        assert isinstance(obj, dict)
        organization_id = UUID(obj.get("organizationId"))
        return SecretIdentifiersRequest(organization_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["organizationId"] = str(self.organization_id)
        return result


@dataclass
class SecretPutRequest:
    """ID of the secret to modify"""
    id: UUID
    key: str
    note: str
    """Organization ID of the secret to modify"""
    organization_id: UUID
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'SecretPutRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        key = from_str(obj.get("key"))
        note = from_str(obj.get("note"))
        organization_id = UUID(obj.get("organizationId"))
        value = from_str(obj.get("value"))
        return SecretPutRequest(id, key, note, organization_id, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["key"] = from_str(self.key)
        result["note"] = from_str(self.note)
        result["organizationId"] = str(self.organization_id)
        result["value"] = from_str(self.value)
        return result


@dataclass
class SecretsCommand:
    """> Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Retrieve a secret by the provided identifier
    
    Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Creates a new secret in the provided organization using the given data
    
    Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Lists all secret identifiers of the given organization, to then retrieve each
    secret, use `CreateSecret`
    
    Returns:
    [SecretIdentifiersResponse](crate::sdk::response::secrets_response::SecretIdentifiersResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Updates an existing secret with the provided ID using the given data
    
    Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
    
    > Requires Authentication > Requires using an Access Token for login or calling Sync at
    least once Deletes all the secrets whose IDs match the provided ones
    
    Returns:
    [SecretsDeleteResponse](crate::sdk::response::secrets_response::SecretsDeleteResponse)
    """
    get: Optional[SecretGetRequest] = None
    create: Optional[SecretCreateRequest] = None
    list: Optional[SecretIdentifiersRequest] = None
    update: Optional[SecretPutRequest] = None
    delete: Optional[SecretsDeleteRequest] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SecretsCommand':
        assert isinstance(obj, dict)
        get = from_union([SecretGetRequest.from_dict, from_none], obj.get("get"))
        create = from_union([SecretCreateRequest.from_dict, from_none], obj.get("create"))
        list = from_union([SecretIdentifiersRequest.from_dict, from_none], obj.get("list"))
        update = from_union([SecretPutRequest.from_dict, from_none], obj.get("update"))
        delete = from_union([SecretsDeleteRequest.from_dict, from_none], obj.get("delete"))
        return SecretsCommand(get, create, list, update, delete)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.get is not None:
            result["get"] = from_union([lambda x: to_class(SecretGetRequest, x), from_none], self.get)
        if self.create is not None:
            result["create"] = from_union([lambda x: to_class(SecretCreateRequest, x), from_none], self.create)
        if self.list is not None:
            result["list"] = from_union([lambda x: to_class(SecretIdentifiersRequest, x), from_none], self.list)
        if self.update is not None:
            result["update"] = from_union([lambda x: to_class(SecretPutRequest, x), from_none], self.update)
        if self.delete is not None:
            result["delete"] = from_union([lambda x: to_class(SecretsDeleteRequest, x), from_none], self.delete)
        return result


@dataclass
class SyncRequest:
    """Exclude the subdomains from the response, defaults to false"""
    exclude_subdomains: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SyncRequest':
        assert isinstance(obj, dict)
        exclude_subdomains = from_union([from_none, from_bool], obj.get("excludeSubdomains"))
        return SyncRequest(exclude_subdomains)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.exclude_subdomains is not None:
            result["excludeSubdomains"] = from_union([from_none, from_bool], self.exclude_subdomains)
        return result


@dataclass
class FolderCreateRequest:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'FolderCreateRequest':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return FolderCreateRequest(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


@dataclass
class FolderDeleteRequest:
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'FolderDeleteRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return FolderDeleteRequest(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class FolderRequest:
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'FolderRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return FolderRequest(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class FolderUpdateRequest:
    id: UUID
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'FolderUpdateRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        return FolderUpdateRequest(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class FoldersCommandClass:
    """> Requires Authentication > Requires an unlocked vault Creates a new folder with the
    provided data
    
    > Requires Authentication > Requires an unlocked vault and calling Sync at least once
    Lists all folders in the vault
    
    Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
    
    > Requires Authentication > Requires an unlocked vault Updates an existing folder with
    the provided data given its ID
    
    > Requires Authentication > Requires an unlocked vault Deletes the folder associated with
    the provided ID
    """
    create: Optional[FolderCreateRequest] = None
    get: Optional[FolderRequest] = None
    update: Optional[FolderUpdateRequest] = None
    delete: Optional[FolderDeleteRequest] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FoldersCommandClass':
        assert isinstance(obj, dict)
        create = from_union([FolderCreateRequest.from_dict, from_none], obj.get("create"))
        get = from_union([FolderRequest.from_dict, from_none], obj.get("get"))
        update = from_union([FolderUpdateRequest.from_dict, from_none], obj.get("update"))
        delete = from_union([FolderDeleteRequest.from_dict, from_none], obj.get("delete"))
        return FoldersCommandClass(create, get, update, delete)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.create is not None:
            result["create"] = from_union([lambda x: to_class(FolderCreateRequest, x), from_none], self.create)
        if self.get is not None:
            result["get"] = from_union([lambda x: to_class(FolderRequest, x), from_none], self.get)
        if self.update is not None:
            result["update"] = from_union([lambda x: to_class(FolderUpdateRequest, x), from_none], self.update)
        if self.delete is not None:
            result["delete"] = from_union([lambda x: to_class(FolderDeleteRequest, x), from_none], self.delete)
        return result


class SCommand(Enum):
    """> Requires Authentication > Requires an unlocked vault and calling Sync at least once
    Lists all folders in the vault
    
    Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
    
    > Requires Authentication > Requires an unlocked vault and calling Sync at least once
    Lists all items in the vault
    
    Returns: [CipherListResponse](bitwarden::vault::cipher::CipherListResponse)
    """
    LIST = "list"


@dataclass
class CipherCreateRequest:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'CipherCreateRequest':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return CipherCreateRequest(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


@dataclass
class CipherDeleteRequest:
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'CipherDeleteRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return CipherDeleteRequest(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class CipherRequest:
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'CipherRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return CipherRequest(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class CipherUpdateRequest:
    id: UUID
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'CipherUpdateRequest':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        return CipherUpdateRequest(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class ItemsCommandClass:
    """> Requires Authentication > Requires an unlocked vault Creates a new item with the
    provided data
    
    > Requires Authentication > Requires an unlocked vault and calling Sync at least once
    Retrieves a single item in the vault
    
    Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
    
    > Requires Authentication > Requires an unlocked vault Updates an existing item with the
    provided data given its ID
    
    > Requires Authentication > Requires an unlocked vault Deletes the item associated with
    the provided ID
    """
    create: Optional[CipherCreateRequest] = None
    get: Optional[CipherRequest] = None
    update: Optional[CipherUpdateRequest] = None
    delete: Optional[CipherDeleteRequest] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ItemsCommandClass':
        assert isinstance(obj, dict)
        create = from_union([CipherCreateRequest.from_dict, from_none], obj.get("create"))
        get = from_union([CipherRequest.from_dict, from_none], obj.get("get"))
        update = from_union([CipherUpdateRequest.from_dict, from_none], obj.get("update"))
        delete = from_union([CipherDeleteRequest.from_dict, from_none], obj.get("delete"))
        return ItemsCommandClass(create, get, update, delete)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.create is not None:
            result["create"] = from_union([lambda x: to_class(CipherCreateRequest, x), from_none], self.create)
        if self.get is not None:
            result["get"] = from_union([lambda x: to_class(CipherRequest, x), from_none], self.get)
        if self.update is not None:
            result["update"] = from_union([lambda x: to_class(CipherUpdateRequest, x), from_none], self.update)
        if self.delete is not None:
            result["delete"] = from_union([lambda x: to_class(CipherDeleteRequest, x), from_none], self.delete)
        return result


@dataclass
class VaultCommand:
    folders: Optional[Union[FoldersCommandClass, SCommand]] = None
    items: Optional[Union[ItemsCommandClass, SCommand]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'VaultCommand':
        assert isinstance(obj, dict)
        folders = from_union([FoldersCommandClass.from_dict, SCommand, from_none], obj.get("folders"))
        items = from_union([ItemsCommandClass.from_dict, SCommand, from_none], obj.get("items"))
        return VaultCommand(folders, items)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.folders is not None:
            result["folders"] = from_union([lambda x: to_class(FoldersCommandClass, x), lambda x: to_enum(SCommand, x), from_none], self.folders)
        if self.items is not None:
            result["items"] = from_union([lambda x: to_class(ItemsCommandClass, x), lambda x: to_enum(SCommand, x), from_none], self.items)
        return result


@dataclass
class Command:
    """Login with username and password
    
    This command is for initiating an authentication handshake with Bitwarden. Authorization
    may fail due to requiring 2fa or captcha challenge completion despite accurate
    credentials.
    
    This command is not capable of handling authentication requiring 2fa or captcha.
    
    Returns: [PasswordLoginResponse](crate::sdk::auth::response::PasswordLoginResponse)
    
    Login with API Key
    
    This command is for initiating an authentication handshake with Bitwarden.
    
    Returns: [ApiKeyLoginResponse](crate::sdk::auth::response::ApiKeyLoginResponse)
    
    Login with Secrets Manager Access Token
    
    This command is for initiating an authentication handshake with Bitwarden.
    
    Returns: [ApiKeyLoginResponse](crate::sdk::auth::response::ApiKeyLoginResponse)
    
    > Requires Authentication Get the API key of the currently authenticated user
    
    Returns:
    [UserApiKeyResponse](crate::sdk::response::user_api_key_response::UserApiKeyResponse)
    
    Get the user's passphrase
    
    Returns: String
    
    > Requires Authentication Retrieve all user data, ciphers and organizations the user is a
    part of
    
    Returns: [SyncResponse](crate::sdk::response::sync_response::SyncResponse)
    """
    password_login: Optional[PasswordLoginRequest] = None
    api_key_login: Optional[APIKeyLoginRequest] = None
    access_token_login: Optional[AccessTokenLoginRequest] = None
    get_user_api_key: Optional[SecretVerificationRequest] = None
    fingerprint: Optional[FingerprintRequest] = None
    sync: Optional[SyncRequest] = None
    secrets: Optional[SecretsCommand] = None
    projects: Optional[ProjectsCommand] = None
    vault: Optional[VaultCommand] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Command':
        assert isinstance(obj, dict)
        password_login = from_union([PasswordLoginRequest.from_dict, from_none], obj.get("passwordLogin"))
        api_key_login = from_union([APIKeyLoginRequest.from_dict, from_none], obj.get("apiKeyLogin"))
        access_token_login = from_union([AccessTokenLoginRequest.from_dict, from_none], obj.get("accessTokenLogin"))
        get_user_api_key = from_union([SecretVerificationRequest.from_dict, from_none], obj.get("getUserApiKey"))
        fingerprint = from_union([FingerprintRequest.from_dict, from_none], obj.get("fingerprint"))
        sync = from_union([SyncRequest.from_dict, from_none], obj.get("sync"))
        secrets = from_union([SecretsCommand.from_dict, from_none], obj.get("secrets"))
        projects = from_union([ProjectsCommand.from_dict, from_none], obj.get("projects"))
        vault = from_union([VaultCommand.from_dict, from_none], obj.get("vault"))
        return Command(password_login, api_key_login, access_token_login, get_user_api_key, fingerprint, sync, secrets, projects, vault)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.password_login is not None:
            result["passwordLogin"] = from_union([lambda x: to_class(PasswordLoginRequest, x), from_none], self.password_login)
        if self.api_key_login is not None:
            result["apiKeyLogin"] = from_union([lambda x: to_class(APIKeyLoginRequest, x), from_none], self.api_key_login)
        if self.access_token_login is not None:
            result["accessTokenLogin"] = from_union([lambda x: to_class(AccessTokenLoginRequest, x), from_none], self.access_token_login)
        if self.get_user_api_key is not None:
            result["getUserApiKey"] = from_union([lambda x: to_class(SecretVerificationRequest, x), from_none], self.get_user_api_key)
        if self.fingerprint is not None:
            result["fingerprint"] = from_union([lambda x: to_class(FingerprintRequest, x), from_none], self.fingerprint)
        if self.sync is not None:
            result["sync"] = from_union([lambda x: to_class(SyncRequest, x), from_none], self.sync)
        if self.secrets is not None:
            result["secrets"] = from_union([lambda x: to_class(SecretsCommand, x), from_none], self.secrets)
        if self.projects is not None:
            result["projects"] = from_union([lambda x: to_class(ProjectsCommand, x), from_none], self.projects)
        if self.vault is not None:
            result["vault"] = from_union([lambda x: to_class(VaultCommand, x), from_none], self.vault)
        return result


@dataclass
class PurpleAuthenticator:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleAuthenticator':
        assert isinstance(obj, dict)
        return PurpleAuthenticator()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class PurpleDuo:
    host: str
    signature: str

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleDuo':
        assert isinstance(obj, dict)
        host = from_str(obj.get("host"))
        signature = from_str(obj.get("signature"))
        return PurpleDuo(host, signature)

    def to_dict(self) -> dict:
        result: dict = {}
        result["host"] = from_str(self.host)
        result["signature"] = from_str(self.signature)
        return result


@dataclass
class PurpleEmail:
    """The email to request a 2fa TOTP for"""
    email: str

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleEmail':
        assert isinstance(obj, dict)
        email = from_str(obj.get("email"))
        return PurpleEmail(email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_str(self.email)
        return result


@dataclass
class PurpleRemember:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleRemember':
        assert isinstance(obj, dict)
        return PurpleRemember()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class PurpleWebAuthn:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleWebAuthn':
        assert isinstance(obj, dict)
        return PurpleWebAuthn()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class PurpleYubiKey:
    """Whether the stored yubikey supports near field communication"""
    nfc: bool

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleYubiKey':
        assert isinstance(obj, dict)
        nfc = from_bool(obj.get("nfc"))
        return PurpleYubiKey(nfc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nfc"] = from_bool(self.nfc)
        return result


@dataclass
class APIKeyLoginResponseTwoFactorProviders:
    authenticator: Optional[PurpleAuthenticator] = None
    """Duo-backed 2fa"""
    duo: Optional[PurpleDuo] = None
    """Email 2fa"""
    email: Optional[PurpleEmail] = None
    """Duo-backed 2fa operated by an organization the user is a member of"""
    organization_duo: Optional[PurpleDuo] = None
    """Presence indicates the user has stored this device as bypassing 2fa"""
    remember: Optional[PurpleRemember] = None
    """WebAuthn-backed 2fa"""
    web_authn: Optional[PurpleWebAuthn] = None
    """Yubikey-backed 2fa"""
    yubi_key: Optional[PurpleYubiKey] = None

    @staticmethod
    def from_dict(obj: Any) -> 'APIKeyLoginResponseTwoFactorProviders':
        assert isinstance(obj, dict)
        authenticator = from_union([PurpleAuthenticator.from_dict, from_none], obj.get("authenticator"))
        duo = from_union([PurpleDuo.from_dict, from_none], obj.get("duo"))
        email = from_union([PurpleEmail.from_dict, from_none], obj.get("email"))
        organization_duo = from_union([PurpleDuo.from_dict, from_none], obj.get("organizationDuo"))
        remember = from_union([PurpleRemember.from_dict, from_none], obj.get("remember"))
        web_authn = from_union([PurpleWebAuthn.from_dict, from_none], obj.get("webAuthn"))
        yubi_key = from_union([PurpleYubiKey.from_dict, from_none], obj.get("yubiKey"))
        return APIKeyLoginResponseTwoFactorProviders(authenticator, duo, email, organization_duo, remember, web_authn, yubi_key)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.authenticator is not None:
            result["authenticator"] = from_union([lambda x: to_class(PurpleAuthenticator, x), from_none], self.authenticator)
        if self.duo is not None:
            result["duo"] = from_union([lambda x: to_class(PurpleDuo, x), from_none], self.duo)
        if self.email is not None:
            result["email"] = from_union([lambda x: to_class(PurpleEmail, x), from_none], self.email)
        if self.organization_duo is not None:
            result["organizationDuo"] = from_union([lambda x: to_class(PurpleDuo, x), from_none], self.organization_duo)
        if self.remember is not None:
            result["remember"] = from_union([lambda x: to_class(PurpleRemember, x), from_none], self.remember)
        if self.web_authn is not None:
            result["webAuthn"] = from_union([lambda x: to_class(PurpleWebAuthn, x), from_none], self.web_authn)
        if self.yubi_key is not None:
            result["yubiKey"] = from_union([lambda x: to_class(PurpleYubiKey, x), from_none], self.yubi_key)
        return result


@dataclass
class APIKeyLoginResponse:
    authenticated: bool
    """Whether or not the user is required to update their master password"""
    force_password_reset: bool
    """TODO: What does this do?"""
    reset_master_password: bool
    two_factor: Optional[APIKeyLoginResponseTwoFactorProviders] = None

    @staticmethod
    def from_dict(obj: Any) -> 'APIKeyLoginResponse':
        assert isinstance(obj, dict)
        authenticated = from_bool(obj.get("authenticated"))
        force_password_reset = from_bool(obj.get("forcePasswordReset"))
        reset_master_password = from_bool(obj.get("resetMasterPassword"))
        two_factor = from_union([APIKeyLoginResponseTwoFactorProviders.from_dict, from_none], obj.get("twoFactor"))
        return APIKeyLoginResponse(authenticated, force_password_reset, reset_master_password, two_factor)

    def to_dict(self) -> dict:
        result: dict = {}
        result["authenticated"] = from_bool(self.authenticated)
        result["forcePasswordReset"] = from_bool(self.force_password_reset)
        result["resetMasterPassword"] = from_bool(self.reset_master_password)
        if self.two_factor is not None:
            result["twoFactor"] = from_union([lambda x: to_class(APIKeyLoginResponseTwoFactorProviders, x), from_none], self.two_factor)
        return result


@dataclass
class ResponseForAPIKeyLoginResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[APIKeyLoginResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForAPIKeyLoginResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([APIKeyLoginResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForAPIKeyLoginResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(APIKeyLoginResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


class CipherRepromptType(Enum):
    NONE = "None"
    PASSWORD = "Password"


class CipherType(Enum):
    CARD = "Card"
    IDENTITY = "Identity"
    LOGIN = "Login"
    SECURE_NOTE = "SecureNote"


@dataclass
class CipherListView:
    collection_ids: List[UUID]
    creation_date: datetime
    favorite: bool
    id: UUID
    name: str
    reprompt: CipherRepromptType
    revision_date: datetime
    type: CipherType
    deleted_date: Optional[datetime] = None
    folder_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    sub_title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CipherListView':
        assert isinstance(obj, dict)
        collection_ids = from_list(lambda x: UUID(x), obj.get("collectionIds"))
        creation_date = from_datetime(obj.get("creationDate"))
        favorite = from_bool(obj.get("favorite"))
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        reprompt = CipherRepromptType(obj.get("reprompt"))
        revision_date = from_datetime(obj.get("revisionDate"))
        type = CipherType(obj.get("type"))
        deleted_date = from_union([from_none, from_datetime], obj.get("deletedDate"))
        folder_id = from_union([from_none, lambda x: UUID(x)], obj.get("folderId"))
        organization_id = from_union([from_none, lambda x: UUID(x)], obj.get("organizationId"))
        sub_title = from_union([from_none, from_str], obj.get("subTitle"))
        return CipherListView(collection_ids, creation_date, favorite, id, name, reprompt, revision_date, type, deleted_date, folder_id, organization_id, sub_title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["collectionIds"] = from_list(lambda x: str(x), self.collection_ids)
        result["creationDate"] = self.creation_date.isoformat()
        result["favorite"] = from_bool(self.favorite)
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        result["reprompt"] = to_enum(CipherRepromptType, self.reprompt)
        result["revisionDate"] = self.revision_date.isoformat()
        result["type"] = to_enum(CipherType, self.type)
        if self.deleted_date is not None:
            result["deletedDate"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_date)
        if self.folder_id is not None:
            result["folderId"] = from_union([from_none, lambda x: str(x)], self.folder_id)
        if self.organization_id is not None:
            result["organizationId"] = from_union([from_none, lambda x: str(x)], self.organization_id)
        if self.sub_title is not None:
            result["subTitle"] = from_union([from_none, from_str], self.sub_title)
        return result


@dataclass
class CipherListResponse:
    ciphers: List[CipherListView]

    @staticmethod
    def from_dict(obj: Any) -> 'CipherListResponse':
        assert isinstance(obj, dict)
        ciphers = from_list(CipherListView.from_dict, obj.get("ciphers"))
        return CipherListResponse(ciphers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ciphers"] = from_list(lambda x: to_class(CipherListView, x), self.ciphers)
        return result


@dataclass
class ResponseForCipherListResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[CipherListResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForCipherListResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([CipherListResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForCipherListResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(CipherListResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class AttachmentView:
    file_name: Optional[str] = None
    id: Optional[str] = None
    key: Optional[str] = None
    size: Optional[str] = None
    size_name: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AttachmentView':
        assert isinstance(obj, dict)
        file_name = from_union([from_none, from_str], obj.get("fileName"))
        id = from_union([from_none, from_str], obj.get("id"))
        key = from_union([from_none, from_str], obj.get("key"))
        size = from_union([from_none, from_str], obj.get("size"))
        size_name = from_union([from_none, from_str], obj.get("sizeName"))
        url = from_union([from_none, from_str], obj.get("url"))
        return AttachmentView(file_name, id, key, size, size_name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.file_name is not None:
            result["fileName"] = from_union([from_none, from_str], self.file_name)
        if self.id is not None:
            result["id"] = from_union([from_none, from_str], self.id)
        if self.key is not None:
            result["key"] = from_union([from_none, from_str], self.key)
        if self.size is not None:
            result["size"] = from_union([from_none, from_str], self.size)
        if self.size_name is not None:
            result["sizeName"] = from_union([from_none, from_str], self.size_name)
        if self.url is not None:
            result["url"] = from_union([from_none, from_str], self.url)
        return result


@dataclass
class CardView:
    brand: Optional[str] = None
    cardholder_name: Optional[str] = None
    code: Optional[str] = None
    exp_month: Optional[str] = None
    exp_year: Optional[str] = None
    number: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CardView':
        assert isinstance(obj, dict)
        brand = from_union([from_none, from_str], obj.get("brand"))
        cardholder_name = from_union([from_none, from_str], obj.get("cardholderName"))
        code = from_union([from_none, from_str], obj.get("code"))
        exp_month = from_union([from_none, from_str], obj.get("expMonth"))
        exp_year = from_union([from_none, from_str], obj.get("expYear"))
        number = from_union([from_none, from_str], obj.get("number"))
        return CardView(brand, cardholder_name, code, exp_month, exp_year, number)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.brand is not None:
            result["brand"] = from_union([from_none, from_str], self.brand)
        if self.cardholder_name is not None:
            result["cardholderName"] = from_union([from_none, from_str], self.cardholder_name)
        if self.code is not None:
            result["code"] = from_union([from_none, from_str], self.code)
        if self.exp_month is not None:
            result["expMonth"] = from_union([from_none, from_str], self.exp_month)
        if self.exp_year is not None:
            result["expYear"] = from_union([from_none, from_str], self.exp_year)
        if self.number is not None:
            result["number"] = from_union([from_none, from_str], self.number)
        return result


class CardLinkedID(Enum):
    BRAND = "brand"
    CARDHOLDER_NAME = "cardholderName"
    CODE = "code"
    EXP_MONTH = "expMonth"
    EXP_YEAR = "expYear"
    NUMBER = "number"


class IdentityLinkedID(Enum):
    ADDRESS1 = "address1"
    ADDRESS2 = "address2"
    ADDRESS3 = "address3"
    CITY = "city"
    COMPANY = "company"
    COUNTRY = "country"
    EMAIL = "email"
    FIRST_NAME = "firstName"
    FULL_NAME = "fullName"
    LAST_NAME = "lastName"
    LICENSE_NUMBER = "licenseNumber"
    MIDDLE_NAME = "middleName"
    PASSPORT_NUMBER = "passportNumber"
    PHONE = "phone"
    POSTAL_CODE = "postalCode"
    SSN = "ssn"
    STATE = "state"
    TITLE = "title"
    USERNAME = "username"


class LoginLinkedID(Enum):
    PASSWORD = "password"
    USERNAME = "username"


@dataclass
class LinkedIDType:
    login_linked_id: Optional[LoginLinkedID] = None
    card_linked_id: Optional[CardLinkedID] = None
    identity_linked_id: Optional[IdentityLinkedID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LinkedIDType':
        assert isinstance(obj, dict)
        login_linked_id = from_union([LoginLinkedID, from_none], obj.get("loginLinkedId"))
        card_linked_id = from_union([CardLinkedID, from_none], obj.get("cardLinkedId"))
        identity_linked_id = from_union([IdentityLinkedID, from_none], obj.get("identityLinkedId"))
        return LinkedIDType(login_linked_id, card_linked_id, identity_linked_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.login_linked_id is not None:
            result["loginLinkedId"] = from_union([lambda x: to_enum(LoginLinkedID, x), from_none], self.login_linked_id)
        if self.card_linked_id is not None:
            result["cardLinkedId"] = from_union([lambda x: to_enum(CardLinkedID, x), from_none], self.card_linked_id)
        if self.identity_linked_id is not None:
            result["identityLinkedId"] = from_union([lambda x: to_enum(IdentityLinkedID, x), from_none], self.identity_linked_id)
        return result


class FieldType(Enum):
    BOOLEAN = "boolean"
    HIDDEN = "hidden"
    LINKED = "linked"
    TEXT = "text"


@dataclass
class FieldView:
    show_count: bool
    show_value: bool
    type: FieldType
    linked_id: Optional[LinkedIDType] = None
    name: Optional[str] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldView':
        assert isinstance(obj, dict)
        show_count = from_bool(obj.get("showCount"))
        show_value = from_bool(obj.get("showValue"))
        type = FieldType(obj.get("type"))
        linked_id = from_union([LinkedIDType.from_dict, from_none], obj.get("linkedId"))
        name = from_union([from_none, from_str], obj.get("name"))
        value = from_union([from_none, from_str], obj.get("value"))
        return FieldView(show_count, show_value, type, linked_id, name, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["showCount"] = from_bool(self.show_count)
        result["showValue"] = from_bool(self.show_value)
        result["type"] = to_enum(FieldType, self.type)
        if self.linked_id is not None:
            result["linkedId"] = from_union([lambda x: to_class(LinkedIDType, x), from_none], self.linked_id)
        if self.name is not None:
            result["name"] = from_union([from_none, from_str], self.name)
        if self.value is not None:
            result["value"] = from_union([from_none, from_str], self.value)
        return result


@dataclass
class IdentityView:
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    city: Optional[str] = None
    company: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    license_number: Optional[str] = None
    middle_name: Optional[str] = None
    passport_number: Optional[str] = None
    phone: Optional[str] = None
    postal_code: Optional[str] = None
    ssn: Optional[str] = None
    state: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'IdentityView':
        assert isinstance(obj, dict)
        address1 = from_union([from_none, from_str], obj.get("address1"))
        address2 = from_union([from_none, from_str], obj.get("address2"))
        address3 = from_union([from_none, from_str], obj.get("address3"))
        city = from_union([from_none, from_str], obj.get("city"))
        company = from_union([from_none, from_str], obj.get("company"))
        country = from_union([from_none, from_str], obj.get("country"))
        email = from_union([from_none, from_str], obj.get("email"))
        first_name = from_union([from_none, from_str], obj.get("firstName"))
        last_name = from_union([from_none, from_str], obj.get("lastName"))
        license_number = from_union([from_none, from_str], obj.get("licenseNumber"))
        middle_name = from_union([from_none, from_str], obj.get("middleName"))
        passport_number = from_union([from_none, from_str], obj.get("passportNumber"))
        phone = from_union([from_none, from_str], obj.get("phone"))
        postal_code = from_union([from_none, from_str], obj.get("postalCode"))
        ssn = from_union([from_none, from_str], obj.get("ssn"))
        state = from_union([from_none, from_str], obj.get("state"))
        title = from_union([from_none, from_str], obj.get("title"))
        username = from_union([from_none, from_str], obj.get("username"))
        return IdentityView(address1, address2, address3, city, company, country, email, first_name, last_name, license_number, middle_name, passport_number, phone, postal_code, ssn, state, title, username)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.address1 is not None:
            result["address1"] = from_union([from_none, from_str], self.address1)
        if self.address2 is not None:
            result["address2"] = from_union([from_none, from_str], self.address2)
        if self.address3 is not None:
            result["address3"] = from_union([from_none, from_str], self.address3)
        if self.city is not None:
            result["city"] = from_union([from_none, from_str], self.city)
        if self.company is not None:
            result["company"] = from_union([from_none, from_str], self.company)
        if self.country is not None:
            result["country"] = from_union([from_none, from_str], self.country)
        if self.email is not None:
            result["email"] = from_union([from_none, from_str], self.email)
        if self.first_name is not None:
            result["firstName"] = from_union([from_none, from_str], self.first_name)
        if self.last_name is not None:
            result["lastName"] = from_union([from_none, from_str], self.last_name)
        if self.license_number is not None:
            result["licenseNumber"] = from_union([from_none, from_str], self.license_number)
        if self.middle_name is not None:
            result["middleName"] = from_union([from_none, from_str], self.middle_name)
        if self.passport_number is not None:
            result["passportNumber"] = from_union([from_none, from_str], self.passport_number)
        if self.phone is not None:
            result["phone"] = from_union([from_none, from_str], self.phone)
        if self.postal_code is not None:
            result["postalCode"] = from_union([from_none, from_str], self.postal_code)
        if self.ssn is not None:
            result["ssn"] = from_union([from_none, from_str], self.ssn)
        if self.state is not None:
            result["state"] = from_union([from_none, from_str], self.state)
        if self.title is not None:
            result["title"] = from_union([from_none, from_str], self.title)
        if self.username is not None:
            result["username"] = from_union([from_none, from_str], self.username)
        return result


class URIMatchType(Enum):
    DOMAIN = "domain"
    EXACT = "exact"
    HOST = "host"
    NEVER = "never"
    REGULAR_EXPRESSION = "regularExpression"
    STARTS_WITH = "startsWith"


@dataclass
class LoginURIView:
    match: URIMatchType
    uri: str

    @staticmethod
    def from_dict(obj: Any) -> 'LoginURIView':
        assert isinstance(obj, dict)
        match = URIMatchType(obj.get("match"))
        uri = from_str(obj.get("uri"))
        return LoginURIView(match, uri)

    def to_dict(self) -> dict:
        result: dict = {}
        result["match"] = to_enum(URIMatchType, self.match)
        result["uri"] = from_str(self.uri)
        return result


@dataclass
class LoginView:
    autofill_on_page_load: bool
    password: str
    uris: List[LoginURIView]
    username: str
    password_revision_date: Optional[datetime] = None
    totp: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LoginView':
        assert isinstance(obj, dict)
        autofill_on_page_load = from_bool(obj.get("autofillOnPageLoad"))
        password = from_str(obj.get("password"))
        uris = from_list(LoginURIView.from_dict, obj.get("uris"))
        username = from_str(obj.get("username"))
        password_revision_date = from_union([from_none, from_datetime], obj.get("passwordRevisionDate"))
        totp = from_union([from_none, from_str], obj.get("totp"))
        return LoginView(autofill_on_page_load, password, uris, username, password_revision_date, totp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["autofillOnPageLoad"] = from_bool(self.autofill_on_page_load)
        result["password"] = from_str(self.password)
        result["uris"] = from_list(lambda x: to_class(LoginURIView, x), self.uris)
        result["username"] = from_str(self.username)
        if self.password_revision_date is not None:
            result["passwordRevisionDate"] = from_union([from_none, lambda x: x.isoformat()], self.password_revision_date)
        if self.totp is not None:
            result["totp"] = from_union([from_none, from_str], self.totp)
        return result


@dataclass
class PasswordHistoryView:
    last_used_date: datetime
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'PasswordHistoryView':
        assert isinstance(obj, dict)
        last_used_date = from_datetime(obj.get("lastUsedDate"))
        password = from_str(obj.get("password"))
        return PasswordHistoryView(last_used_date, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lastUsedDate"] = self.last_used_date.isoformat()
        result["password"] = from_str(self.password)
        return result


@dataclass
class CipherView:
    attachments: List[AttachmentView]
    collection_ids: List[UUID]
    creation_date: datetime
    favorite: bool
    fields: List[FieldView]
    id: UUID
    name: str
    notes: str
    password_history: List[PasswordHistoryView]
    reprompt: CipherRepromptType
    revision_date: datetime
    type: CipherType
    card: Optional[CardView] = None
    deleted_date: Optional[datetime] = None
    folder_id: Optional[UUID] = None
    identity: Optional[IdentityView] = None
    login: Optional[LoginView] = None
    organization_id: Optional[UUID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CipherView':
        assert isinstance(obj, dict)
        attachments = from_list(AttachmentView.from_dict, obj.get("attachments"))
        collection_ids = from_list(lambda x: UUID(x), obj.get("collectionIds"))
        creation_date = from_datetime(obj.get("creationDate"))
        favorite = from_bool(obj.get("favorite"))
        fields = from_list(FieldView.from_dict, obj.get("fields"))
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        notes = from_str(obj.get("notes"))
        password_history = from_list(PasswordHistoryView.from_dict, obj.get("passwordHistory"))
        reprompt = CipherRepromptType(obj.get("reprompt"))
        revision_date = from_datetime(obj.get("revisionDate"))
        type = CipherType(obj.get("type"))
        card = from_union([CardView.from_dict, from_none], obj.get("card"))
        deleted_date = from_union([from_none, from_datetime], obj.get("deletedDate"))
        folder_id = from_union([from_none, lambda x: UUID(x)], obj.get("folderId"))
        identity = from_union([IdentityView.from_dict, from_none], obj.get("identity"))
        login = from_union([LoginView.from_dict, from_none], obj.get("login"))
        organization_id = from_union([from_none, lambda x: UUID(x)], obj.get("organizationId"))
        return CipherView(attachments, collection_ids, creation_date, favorite, fields, id, name, notes, password_history, reprompt, revision_date, type, card, deleted_date, folder_id, identity, login, organization_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attachments"] = from_list(lambda x: to_class(AttachmentView, x), self.attachments)
        result["collectionIds"] = from_list(lambda x: str(x), self.collection_ids)
        result["creationDate"] = self.creation_date.isoformat()
        result["favorite"] = from_bool(self.favorite)
        result["fields"] = from_list(lambda x: to_class(FieldView, x), self.fields)
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        result["notes"] = from_str(self.notes)
        result["passwordHistory"] = from_list(lambda x: to_class(PasswordHistoryView, x), self.password_history)
        result["reprompt"] = to_enum(CipherRepromptType, self.reprompt)
        result["revisionDate"] = self.revision_date.isoformat()
        result["type"] = to_enum(CipherType, self.type)
        if self.card is not None:
            result["card"] = from_union([lambda x: to_class(CardView, x), from_none], self.card)
        if self.deleted_date is not None:
            result["deletedDate"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_date)
        if self.folder_id is not None:
            result["folderId"] = from_union([from_none, lambda x: str(x)], self.folder_id)
        if self.identity is not None:
            result["identity"] = from_union([lambda x: to_class(IdentityView, x), from_none], self.identity)
        if self.login is not None:
            result["login"] = from_union([lambda x: to_class(LoginView, x), from_none], self.login)
        if self.organization_id is not None:
            result["organizationId"] = from_union([from_none, lambda x: str(x)], self.organization_id)
        return result


@dataclass
class ResponseForCipherView:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[CipherView] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForCipherView':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([CipherView.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForCipherView(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(CipherView, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class FolderView:
    id: UUID
    name: str
    revision_date: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'FolderView':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        revision_date = from_datetime(obj.get("revisionDate"))
        return FolderView(id, name, revision_date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        result["revisionDate"] = self.revision_date.isoformat()
        return result


@dataclass
class FolderResponse:
    folder: FolderView

    @staticmethod
    def from_dict(obj: Any) -> 'FolderResponse':
        assert isinstance(obj, dict)
        folder = FolderView.from_dict(obj.get("folder"))
        return FolderResponse(folder)

    def to_dict(self) -> dict:
        result: dict = {}
        result["folder"] = to_class(FolderView, self.folder)
        return result


@dataclass
class ResponseForFolderResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[FolderResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForFolderResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([FolderResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForFolderResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(FolderResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class CAPTCHAResponse:
    """hcaptcha site key"""
    site_key: str

    @staticmethod
    def from_dict(obj: Any) -> 'CAPTCHAResponse':
        assert isinstance(obj, dict)
        site_key = from_str(obj.get("siteKey"))
        return CAPTCHAResponse(site_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["siteKey"] = from_str(self.site_key)
        return result


@dataclass
class FluffyAuthenticator:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyAuthenticator':
        assert isinstance(obj, dict)
        return FluffyAuthenticator()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class FluffyDuo:
    host: str
    signature: str

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyDuo':
        assert isinstance(obj, dict)
        host = from_str(obj.get("host"))
        signature = from_str(obj.get("signature"))
        return FluffyDuo(host, signature)

    def to_dict(self) -> dict:
        result: dict = {}
        result["host"] = from_str(self.host)
        result["signature"] = from_str(self.signature)
        return result


@dataclass
class FluffyEmail:
    """The email to request a 2fa TOTP for"""
    email: str

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyEmail':
        assert isinstance(obj, dict)
        email = from_str(obj.get("email"))
        return FluffyEmail(email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_str(self.email)
        return result


@dataclass
class FluffyRemember:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyRemember':
        assert isinstance(obj, dict)
        return FluffyRemember()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class FluffyWebAuthn:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyWebAuthn':
        assert isinstance(obj, dict)
        return FluffyWebAuthn()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class FluffyYubiKey:
    """Whether the stored yubikey supports near field communication"""
    nfc: bool

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyYubiKey':
        assert isinstance(obj, dict)
        nfc = from_bool(obj.get("nfc"))
        return FluffyYubiKey(nfc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nfc"] = from_bool(self.nfc)
        return result


@dataclass
class PasswordLoginResponseTwoFactorProviders:
    authenticator: Optional[FluffyAuthenticator] = None
    """Duo-backed 2fa"""
    duo: Optional[FluffyDuo] = None
    """Email 2fa"""
    email: Optional[FluffyEmail] = None
    """Duo-backed 2fa operated by an organization the user is a member of"""
    organization_duo: Optional[FluffyDuo] = None
    """Presence indicates the user has stored this device as bypassing 2fa"""
    remember: Optional[FluffyRemember] = None
    """WebAuthn-backed 2fa"""
    web_authn: Optional[FluffyWebAuthn] = None
    """Yubikey-backed 2fa"""
    yubi_key: Optional[FluffyYubiKey] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PasswordLoginResponseTwoFactorProviders':
        assert isinstance(obj, dict)
        authenticator = from_union([FluffyAuthenticator.from_dict, from_none], obj.get("authenticator"))
        duo = from_union([FluffyDuo.from_dict, from_none], obj.get("duo"))
        email = from_union([FluffyEmail.from_dict, from_none], obj.get("email"))
        organization_duo = from_union([FluffyDuo.from_dict, from_none], obj.get("organizationDuo"))
        remember = from_union([FluffyRemember.from_dict, from_none], obj.get("remember"))
        web_authn = from_union([FluffyWebAuthn.from_dict, from_none], obj.get("webAuthn"))
        yubi_key = from_union([FluffyYubiKey.from_dict, from_none], obj.get("yubiKey"))
        return PasswordLoginResponseTwoFactorProviders(authenticator, duo, email, organization_duo, remember, web_authn, yubi_key)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.authenticator is not None:
            result["authenticator"] = from_union([lambda x: to_class(FluffyAuthenticator, x), from_none], self.authenticator)
        if self.duo is not None:
            result["duo"] = from_union([lambda x: to_class(FluffyDuo, x), from_none], self.duo)
        if self.email is not None:
            result["email"] = from_union([lambda x: to_class(FluffyEmail, x), from_none], self.email)
        if self.organization_duo is not None:
            result["organizationDuo"] = from_union([lambda x: to_class(FluffyDuo, x), from_none], self.organization_duo)
        if self.remember is not None:
            result["remember"] = from_union([lambda x: to_class(FluffyRemember, x), from_none], self.remember)
        if self.web_authn is not None:
            result["webAuthn"] = from_union([lambda x: to_class(FluffyWebAuthn, x), from_none], self.web_authn)
        if self.yubi_key is not None:
            result["yubiKey"] = from_union([lambda x: to_class(FluffyYubiKey, x), from_none], self.yubi_key)
        return result


@dataclass
class PasswordLoginResponse:
    authenticated: bool
    """Whether or not the user is required to update their master password"""
    force_password_reset: bool
    """TODO: What does this do?"""
    reset_master_password: bool
    """The information required to present the user with a captcha challenge. Only present when
    authentication fails due to requiring validation of a captcha challenge.
    """
    captcha: Optional[CAPTCHAResponse] = None
    """The available two factor authentication options. Present only when authentication fails
    due to requiring a second authentication factor.
    """
    two_factor: Optional[PasswordLoginResponseTwoFactorProviders] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PasswordLoginResponse':
        assert isinstance(obj, dict)
        authenticated = from_bool(obj.get("authenticated"))
        force_password_reset = from_bool(obj.get("forcePasswordReset"))
        reset_master_password = from_bool(obj.get("resetMasterPassword"))
        captcha = from_union([CAPTCHAResponse.from_dict, from_none], obj.get("captcha"))
        two_factor = from_union([PasswordLoginResponseTwoFactorProviders.from_dict, from_none], obj.get("twoFactor"))
        return PasswordLoginResponse(authenticated, force_password_reset, reset_master_password, captcha, two_factor)

    def to_dict(self) -> dict:
        result: dict = {}
        result["authenticated"] = from_bool(self.authenticated)
        result["forcePasswordReset"] = from_bool(self.force_password_reset)
        result["resetMasterPassword"] = from_bool(self.reset_master_password)
        if self.captcha is not None:
            result["captcha"] = from_union([lambda x: to_class(CAPTCHAResponse, x), from_none], self.captcha)
        if self.two_factor is not None:
            result["twoFactor"] = from_union([lambda x: to_class(PasswordLoginResponseTwoFactorProviders, x), from_none], self.two_factor)
        return result


@dataclass
class ResponseForPasswordLoginResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[PasswordLoginResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForPasswordLoginResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([PasswordLoginResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForPasswordLoginResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(PasswordLoginResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class SecretIdentifierResponse:
    id: UUID
    key: str
    organization_id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'SecretIdentifierResponse':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        key = from_str(obj.get("key"))
        organization_id = UUID(obj.get("organizationId"))
        return SecretIdentifierResponse(id, key, organization_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["key"] = from_str(self.key)
        result["organizationId"] = str(self.organization_id)
        return result


@dataclass
class SecretIdentifiersResponse:
    data: List[SecretIdentifierResponse]

    @staticmethod
    def from_dict(obj: Any) -> 'SecretIdentifiersResponse':
        assert isinstance(obj, dict)
        data = from_list(SecretIdentifierResponse.from_dict, obj.get("data"))
        return SecretIdentifiersResponse(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: to_class(SecretIdentifierResponse, x), self.data)
        return result


@dataclass
class ResponseForSecretIdentifiersResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[SecretIdentifiersResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForSecretIdentifiersResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([SecretIdentifiersResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForSecretIdentifiersResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(SecretIdentifiersResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class SecretResponse:
    creation_date: str
    id: UUID
    key: str
    note: str
    object: str
    organization_id: UUID
    revision_date: str
    value: str
    project_id: Optional[UUID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SecretResponse':
        assert isinstance(obj, dict)
        creation_date = from_str(obj.get("creationDate"))
        id = UUID(obj.get("id"))
        key = from_str(obj.get("key"))
        note = from_str(obj.get("note"))
        object = from_str(obj.get("object"))
        organization_id = UUID(obj.get("organizationId"))
        revision_date = from_str(obj.get("revisionDate"))
        value = from_str(obj.get("value"))
        project_id = from_union([from_none, lambda x: UUID(x)], obj.get("projectId"))
        return SecretResponse(creation_date, id, key, note, object, organization_id, revision_date, value, project_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["creationDate"] = from_str(self.creation_date)
        result["id"] = str(self.id)
        result["key"] = from_str(self.key)
        result["note"] = from_str(self.note)
        result["object"] = from_str(self.object)
        result["organizationId"] = str(self.organization_id)
        result["revisionDate"] = from_str(self.revision_date)
        result["value"] = from_str(self.value)
        if self.project_id is not None:
            result["projectId"] = from_union([from_none, lambda x: str(x)], self.project_id)
        return result


@dataclass
class ResponseForSecretResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[SecretResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForSecretResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([SecretResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForSecretResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(SecretResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class SecretDeleteResponse:
    id: UUID
    error: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SecretDeleteResponse':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        error = from_union([from_none, from_str], obj.get("error"))
        return SecretDeleteResponse(id, error)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        if self.error is not None:
            result["error"] = from_union([from_none, from_str], self.error)
        return result


@dataclass
class SecretsDeleteResponse:
    data: List[SecretDeleteResponse]

    @staticmethod
    def from_dict(obj: Any) -> 'SecretsDeleteResponse':
        assert isinstance(obj, dict)
        data = from_list(SecretDeleteResponse.from_dict, obj.get("data"))
        return SecretsDeleteResponse(data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: to_class(SecretDeleteResponse, x), self.data)
        return result


@dataclass
class ResponseForSecretsDeleteResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[SecretsDeleteResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForSecretsDeleteResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([SecretsDeleteResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForSecretsDeleteResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(SecretsDeleteResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class CipherDetailsResponse:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'CipherDetailsResponse':
        assert isinstance(obj, dict)
        return CipherDetailsResponse()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class ProfileOrganizationResponse:
    id: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'ProfileOrganizationResponse':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return ProfileOrganizationResponse(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


@dataclass
class ProfileResponse:
    """Data about the user, including their encryption keys and the organizations they are a
    part of
    """
    email: str
    id: UUID
    name: str
    organizations: List[ProfileOrganizationResponse]

    @staticmethod
    def from_dict(obj: Any) -> 'ProfileResponse':
        assert isinstance(obj, dict)
        email = from_str(obj.get("email"))
        id = UUID(obj.get("id"))
        name = from_str(obj.get("name"))
        organizations = from_list(ProfileOrganizationResponse.from_dict, obj.get("organizations"))
        return ProfileResponse(email, id, name, organizations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_str(self.email)
        result["id"] = str(self.id)
        result["name"] = from_str(self.name)
        result["organizations"] = from_list(lambda x: to_class(ProfileOrganizationResponse, x), self.organizations)
        return result


@dataclass
class SyncResponse:
    """List of ciphers accesible by the user"""
    ciphers: List[CipherDetailsResponse]
    """Data about the user, including their encryption keys and the organizations they are a
    part of
    """
    profile: ProfileResponse

    @staticmethod
    def from_dict(obj: Any) -> 'SyncResponse':
        assert isinstance(obj, dict)
        ciphers = from_list(CipherDetailsResponse.from_dict, obj.get("ciphers"))
        profile = ProfileResponse.from_dict(obj.get("profile"))
        return SyncResponse(ciphers, profile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ciphers"] = from_list(lambda x: to_class(CipherDetailsResponse, x), self.ciphers)
        result["profile"] = to_class(ProfileResponse, self.profile)
        return result


@dataclass
class ResponseForSyncResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[SyncResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForSyncResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([SyncResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForSyncResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(SyncResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


@dataclass
class UserAPIKeyResponse:
    """The user's API key, which represents the client_secret portion of an oauth request."""
    api_key: str

    @staticmethod
    def from_dict(obj: Any) -> 'UserAPIKeyResponse':
        assert isinstance(obj, dict)
        api_key = from_str(obj.get("apiKey"))
        return UserAPIKeyResponse(api_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["apiKey"] = from_str(self.api_key)
        return result


@dataclass
class ResponseForUserAPIKeyResponse:
    """Whether or not the SDK request succeeded."""
    success: bool
    """The response data. Populated if `success` is true."""
    data: Optional[UserAPIKeyResponse] = None
    """A message for any error that may occur. Populated if `success` is false."""
    error_message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseForUserAPIKeyResponse':
        assert isinstance(obj, dict)
        success = from_bool(obj.get("success"))
        data = from_union([UserAPIKeyResponse.from_dict, from_none], obj.get("data"))
        error_message = from_union([from_none, from_str], obj.get("errorMessage"))
        return ResponseForUserAPIKeyResponse(success, data, error_message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_bool(self.success)
        if self.data is not None:
            result["data"] = from_union([lambda x: to_class(UserAPIKeyResponse, x), from_none], self.data)
        if self.error_message is not None:
            result["errorMessage"] = from_union([from_none, from_str], self.error_message)
        return result


def client_settings_from_dict(s: Any) -> ClientSettings:
    return ClientSettings.from_dict(s)


def client_settings_to_dict(x: ClientSettings) -> Any:
    return to_class(ClientSettings, x)


def command_from_dict(s: Any) -> Command:
    return Command.from_dict(s)


def command_to_dict(x: Command) -> Any:
    return to_class(Command, x)


def response_for_api_key_login_response_from_dict(s: Any) -> ResponseForAPIKeyLoginResponse:
    return ResponseForAPIKeyLoginResponse.from_dict(s)


def response_for_api_key_login_response_to_dict(x: ResponseForAPIKeyLoginResponse) -> Any:
    return to_class(ResponseForAPIKeyLoginResponse, x)


def response_for_cipher_list_response_from_dict(s: Any) -> ResponseForCipherListResponse:
    return ResponseForCipherListResponse.from_dict(s)


def response_for_cipher_list_response_to_dict(x: ResponseForCipherListResponse) -> Any:
    return to_class(ResponseForCipherListResponse, x)


def response_for_cipher_view_from_dict(s: Any) -> ResponseForCipherView:
    return ResponseForCipherView.from_dict(s)


def response_for_cipher_view_to_dict(x: ResponseForCipherView) -> Any:
    return to_class(ResponseForCipherView, x)


def response_for_folder_response_from_dict(s: Any) -> ResponseForFolderResponse:
    return ResponseForFolderResponse.from_dict(s)


def response_for_folder_response_to_dict(x: ResponseForFolderResponse) -> Any:
    return to_class(ResponseForFolderResponse, x)


def response_for_password_login_response_from_dict(s: Any) -> ResponseForPasswordLoginResponse:
    return ResponseForPasswordLoginResponse.from_dict(s)


def response_for_password_login_response_to_dict(x: ResponseForPasswordLoginResponse) -> Any:
    return to_class(ResponseForPasswordLoginResponse, x)


def response_for_secret_identifiers_response_from_dict(s: Any) -> ResponseForSecretIdentifiersResponse:
    return ResponseForSecretIdentifiersResponse.from_dict(s)


def response_for_secret_identifiers_response_to_dict(x: ResponseForSecretIdentifiersResponse) -> Any:
    return to_class(ResponseForSecretIdentifiersResponse, x)


def response_for_secret_response_from_dict(s: Any) -> ResponseForSecretResponse:
    return ResponseForSecretResponse.from_dict(s)


def response_for_secret_response_to_dict(x: ResponseForSecretResponse) -> Any:
    return to_class(ResponseForSecretResponse, x)


def response_for_secrets_delete_response_from_dict(s: Any) -> ResponseForSecretsDeleteResponse:
    return ResponseForSecretsDeleteResponse.from_dict(s)


def response_for_secrets_delete_response_to_dict(x: ResponseForSecretsDeleteResponse) -> Any:
    return to_class(ResponseForSecretsDeleteResponse, x)


def response_for_sync_response_from_dict(s: Any) -> ResponseForSyncResponse:
    return ResponseForSyncResponse.from_dict(s)


def response_for_sync_response_to_dict(x: ResponseForSyncResponse) -> Any:
    return to_class(ResponseForSyncResponse, x)


def response_for_user_api_key_response_from_dict(s: Any) -> ResponseForUserAPIKeyResponse:
    return ResponseForUserAPIKeyResponse.from_dict(s)


def response_for_user_api_key_response_to_dict(x: ResponseForUserAPIKeyResponse) -> Any:
    return to_class(ResponseForUserAPIKeyResponse, x)

