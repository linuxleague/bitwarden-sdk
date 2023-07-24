use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
#[cfg_attr(feature = "use_uniffi", derive(uniffi::Record))]
pub struct Duo {
    pub host: String,
    pub signature: String,
}

impl From<crate::auth::api::response::two_factor_provider_data::duo::Duo> for Duo {
    fn from(api: crate::auth::api::response::two_factor_provider_data::duo::Duo) -> Self {
        Self {
            host: api.host,
            signature: api.signature,
        }
    }
}

impl From<crate::auth::api::response::two_factor_provider_data::organization_duo::OrganizationDuo>
    for Duo
{
    fn from(
        api: crate::auth::api::response::two_factor_provider_data::organization_duo::OrganizationDuo,
    ) -> Self {
        Self {
            host: api.host,
            signature: api.signature,
        }
    }
}
