use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

/// Login to Bitwarden with Username and Password
#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
#[cfg_attr(feature = "use_uniffi", derive(uniffi::Record))]
pub struct PasswordLoginRequest {
    /// Bitwarden account email address
    pub email: String,
    /// Bitwarden account master password
    pub password: String,
}
