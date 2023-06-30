use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use bitwarden::{
    auth::request::AccessTokenLoginRequest,
    secrets_manager::{
        projects::{
            ProjectCreateRequest, ProjectGetRequest, ProjectPutRequest, ProjectsDeleteRequest,
            ProjectsListRequest,
        },
        secrets::{
            SecretCreateRequest, SecretGetRequest, SecretIdentifiersRequest, SecretPutRequest,
            SecretsDeleteRequest,
        },
    },
};
#[cfg(feature = "internal")]
use bitwarden::{
    auth::request::{ApiKeyLoginRequest, PasswordLoginRequest},
    platform::{FingerprintRequest, SecretVerificationRequest, SyncRequest},
    vault::{
        CipherCreateRequest, CipherDeleteRequest, CipherRequest, CipherUpdateRequest,
        FolderCreateRequest, FolderDeleteRequest, FolderRequest, FolderUpdateRequest,
    },
};

#[derive(Serialize, Deserialize, JsonSchema, Debug)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum Command {
    #[cfg(feature = "internal")]
    /// Login with username and password
    ///
    /// This command is for initiating an authentication handshake with Bitwarden.
    /// Authorization may fail due to requiring 2fa or captcha challenge completion
    /// despite accurate credentials.
    ///
    /// This command is not capable of handling authentication requiring 2fa or captcha.
    ///
    /// Returns: [PasswordLoginResponse](crate::sdk::auth::response::PasswordLoginResponse)
    ///
    PasswordLogin(PasswordLoginRequest),

    #[cfg(feature = "internal")]
    /// Login with API Key
    ///
    /// This command is for initiating an authentication handshake with Bitwarden.
    ///
    /// Returns: [ApiKeyLoginResponse](crate::sdk::auth::response::ApiKeyLoginResponse)
    ///
    ApiKeyLogin(ApiKeyLoginRequest),

    /// Login with Secrets Manager Access Token
    ///
    /// This command is for initiating an authentication handshake with Bitwarden.
    ///
    /// Returns: [ApiKeyLoginResponse](crate::sdk::auth::response::ApiKeyLoginResponse)
    ///
    AccessTokenLogin(AccessTokenLoginRequest),

    #[cfg(feature = "internal")]
    /// > Requires Authentication
    /// Get the API key of the currently authenticated user
    ///
    /// Returns: [UserApiKeyResponse](crate::sdk::response::user_api_key_response::UserApiKeyResponse)
    ///
    GetUserApiKey(SecretVerificationRequest),

    #[cfg(feature = "internal")]
    /// Get the user's passphrase
    ///
    /// Returns: String
    ///
    Fingerprint(FingerprintRequest),

    #[cfg(feature = "internal")]
    /// > Requires Authentication
    /// Retrieve all user data, ciphers and organizations the user is a part of
    ///
    /// Returns: [SyncResponse](crate::sdk::response::sync_response::SyncResponse)
    ///
    Sync(SyncRequest),

    Secrets(SecretsCommand),
    Projects(ProjectsCommand),

    #[cfg(feature = "internal")]
    Vault(VaultCommand),
}

#[derive(Serialize, Deserialize, JsonSchema, Debug)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum SecretsCommand {
    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Retrieve a secret by the provided identifier
    ///
    /// Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
    ///
    Get(SecretGetRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Creates a new secret in the provided organization using the given data
    ///
    /// Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
    ///
    Create(SecretCreateRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Lists all secret identifiers of the given organization, to then retrieve each secret, use `CreateSecret`
    ///
    /// Returns: [SecretIdentifiersResponse](crate::sdk::response::secrets_response::SecretIdentifiersResponse)
    ///
    List(SecretIdentifiersRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Updates an existing secret with the provided ID using the given data
    ///
    /// Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
    ///
    Update(SecretPutRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Deletes all the secrets whose IDs match the provided ones
    ///
    /// Returns: [SecretsDeleteResponse](crate::sdk::response::secrets_response::SecretsDeleteResponse)
    ///
    Delete(SecretsDeleteRequest),
}

#[derive(Serialize, Deserialize, JsonSchema, Debug)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum ProjectsCommand {
    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Retrieve a project by the provided identifier
    ///
    /// Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
    ///
    Get(ProjectGetRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Creates a new project in the provided organization using the given data
    ///
    /// Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
    ///
    Create(ProjectCreateRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Lists all projects of the given organization
    ///
    /// Returns: [ProjectsResponse](crate::sdk::response::projects_response::ProjectsResponse)
    ///
    List(ProjectsListRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Updates an existing project with the provided ID using the given data
    ///
    /// Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
    ///
    Update(ProjectPutRequest),

    /// > Requires Authentication
    /// > Requires using an Access Token for login or calling Sync at least once
    /// Deletes all the projects whose IDs match the provided ones
    ///
    /// Returns: [ProjectsDeleteResponse](crate::sdk::response::projects_response::ProjectsDeleteResponse)
    ///
    Delete(ProjectsDeleteRequest),
}

#[cfg(feature = "internal")]
#[derive(Serialize, Deserialize, JsonSchema, Debug)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum VaultCommand {
    Folders(FoldersCommand),
    Items(ItemsCommand),
}

#[cfg(feature = "internal")]
#[derive(Serialize, Deserialize, JsonSchema, Debug)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum FoldersCommand {
    /// > Requires Authentication
    /// > Requires an unlocked vault
    /// Creates a new folder with the provided data
    ///
    Create(FolderCreateRequest),

    /// > Requires Authentication
    /// > Requires an unlocked vault and calling Sync at least once
    /// Lists all folders in the vault
    ///
    /// Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
    ///
    List,

    /// > Requires Authentication
    /// > Requires an unlocked vault and calling Sync at least once
    /// Lists all folders in the vault
    ///
    /// Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
    ///
    Get(FolderRequest),

    /// > Requires Authentication
    /// > Requires an unlocked vault
    /// Updates an existing folder with the provided data given its ID
    ///
    Update(FolderUpdateRequest),

    /// > Requires Authentication
    /// > Requires an unlocked vault
    /// Deletes the folder associated with the provided ID
    ///
    Delete(FolderDeleteRequest),
}

#[cfg(feature = "internal")]
#[derive(Serialize, Deserialize, JsonSchema, Debug)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum ItemsCommand {
    /// > Requires Authentication
    /// > Requires an unlocked vault
    /// Creates a new item with the provided data
    ///
    Create(CipherCreateRequest),

    /// > Requires Authentication
    /// > Requires an unlocked vault and calling Sync at least once
    /// Lists all items in the vault
    ///
    /// Returns: [CipherListResponse](bitwarden::vault::cipher::CipherListResponse)
    ///
    List,

    /// > Requires Authentication
    /// > Requires an unlocked vault and calling Sync at least once
    /// Retrieves a single item in the vault
    ///
    /// Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
    ///
    Get(CipherRequest),

    /// > Requires Authentication
    /// > Requires an unlocked vault
    /// Updates an existing item with the provided data given its ID
    ///
    Update(CipherUpdateRequest),

    /// > Requires Authentication
    /// > Requires an unlocked vault
    /// Deletes the item associated with the provided ID
    ///
    Delete(CipherDeleteRequest),
}
