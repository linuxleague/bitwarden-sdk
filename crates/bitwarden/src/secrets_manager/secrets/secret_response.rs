use bitwarden_api_api::models::SecretResponseModel;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::{
    client::encryption_settings::EncryptionSettings,
    crypto::{CipherString, Decryptable},
    error::{Error, Result},
};

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SecretResponse {
    pub object: String,
    pub id: Uuid,
    pub organization_id: Uuid,
    pub project_id: Option<Uuid>,

    pub key: String,
    pub value: String,
    pub note: String,

    pub creation_date: String,
    pub revision_date: String,
}

impl SecretResponse {
    pub(crate) fn process_response(
        response: SecretResponseModel,
        enc: &EncryptionSettings,
    ) -> Result<SecretResponse> {
        let org_id = response.organization_id;

        let key = response
            .key
            .ok_or(Error::MissingFields)?
            .parse::<CipherString>()?
            .decrypt(enc, &org_id)?;
        let value = response
            .value
            .ok_or(Error::MissingFields)?
            .parse::<CipherString>()?
            .decrypt(enc, &org_id)?;
        let note = response
            .note
            .ok_or(Error::MissingFields)?
            .parse::<CipherString>()?
            .decrypt(enc, &org_id)?;

        let project = response
            .projects
            .and_then(|p| p.into_iter().next())
            .and_then(|p| p.id);

        Ok(SecretResponse {
            object: "secret".to_owned(),
            id: response.id.ok_or(Error::MissingFields)?,
            organization_id: org_id.ok_or(Error::MissingFields)?,
            project_id: project,
            key,
            value,
            note,

            creation_date: response.creation_date.ok_or(Error::MissingFields)?,
            revision_date: response.revision_date.ok_or(Error::MissingFields)?,
        })
    }
}
