use bitwarden_api_identity::{
    apis::accounts_api::accounts_register_post,
    models::{KeysRequestModel, RegisterRequestModel},
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::{
    auth,
    client::auth_settings::{AuthSettings, Kdf},
    error::Result,
    util::default_pbkdf2_iterations,
    Client,
};

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct RegisterRequest {
    pub email: String,
    pub name: Option<String>,
    pub password: String,
    pub password_hint: Option<String>,
}

pub(crate) async fn register(
    client: &mut Client,
    req: &RegisterRequest,
) -> Result<RegisterResponse> {
    let config = client.get_api_configurations().await;

    let auth_settings = AuthSettings {
        email: req.email.to_owned(),
        kdf: Kdf::PBKDF2 {
            iterations: default_pbkdf2_iterations(),
        },
    };

    let key = auth_settings.make_master_key(&req.password, &req.email)?;
    let master_password_hash = auth_settings.make_password_hash(&req.password, key)?;
    let user_key = auth_settings.make_user_key(key)?;
    let keys = auth_settings.make_key_pair(user_key.0)?;

    // key = await this.cryptoService.makeMasterKey(masterPassword, email, kdf, kdfConfig);
    // newUserKey = await this.cryptoService.makeUserKey(key);
    // masterKeyHash = await this.cryptoService.hashMasterKey(masterPassword, key);
    // keys = await this.cryptoService.makeKeyPair(newUserKey[0]);

    accounts_register_post(
        &config.identity,
        Some(RegisterRequestModel {
            name: req.name.to_owned(),
            email: req.email.to_owned(),
            master_password_hash,
            master_password_hint: req.password_hint.to_owned(),
            captcha_response: None, // TODO: Add
            key: Some(user_key.1.to_string()),
            keys: Some(Box::new(KeysRequestModel {
                public_key: Some(keys.0),
                encrypted_private_key: keys.1.to_string(),
            })),

            token: None,
            organization_user_id: None,
            kdf: Some(bitwarden_api_identity::models::KdfType::Variant0),
            kdf_iterations: Some(default_pbkdf2_iterations().get() as i32),
            kdf_memory: None,
            kdf_parallelism: None,
            reference_data: None, // TODO: Add

                                  /*
                                  newUserKey[1].encryptedString,
                                  this.referenceData,
                                  kdf,
                                  kdfConfig.iterations,
                                  kdfConfig.memory,
                                  kdfConfig.parallelism
                                  */
        }),
    )
    .await?;

    unimplemented!()
}

pub struct RegisterResponse {}