use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

/// Login to Bitwarden with Api Key
#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
#[cfg_attr(feature = "use_uniffi", derive(uniffi::Record))]
pub struct ApiKeyLoginRequest {
    /// Bitwarden account client_id
    pub client_id: String,
    /// Bitwarden account client_secret
    pub client_secret: String,

    /// Bitwarden account master password
    pub password: String,
}

/// Login to Bitwarden with access token
#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
#[cfg_attr(feature = "use_uniffi", derive(uniffi::Record))]
pub struct AccessTokenLoginRequest {
    /// Bitwarden service API access token
    pub access_token: String,
}
