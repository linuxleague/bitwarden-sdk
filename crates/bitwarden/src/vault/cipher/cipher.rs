use super::{card, identity, login};
use chrono::{DateTime, Utc};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
pub enum CipherType {
    Login = 1,
    SecureNote = 2,
    Card = 3,
    Identity = 4,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
pub enum CipherRepromptType {
    None = 0,
    Password = 1,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherListView {
    pub id: Uuid,
    pub organization_id: Option<Uuid>,
    pub folder_id: Option<Uuid>,

    pub name: String,
    pub sub_title: Option<String>,

    pub r#type: CipherType,

    pub collection_ids: Vec<Uuid>,
    pub favorite: bool,
    pub reprompt: CipherRepromptType,

    pub creation_date: DateTime<Utc>,
    pub deleted_date: Option<DateTime<Utc>>,
    pub revision_date: DateTime<Utc>,
}

// #[derive(Serialize, Deserialize, Debug, JsonSchema)]
// #[serde(rename_all = "camelCase", deny_unknown_fields)]
// pub enum SecureNoteType {
//     Generic = 0,
// }

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct AttachmentView {
    pub id: Option<String>,
    pub url: Option<String>,
    pub size: Option<String>,
    pub size_name: Option<String>,
    pub file_name: Option<String>,
    pub key: Option<String>, // TODO: Should be a key
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum FieldType {
    Text = 0,
    Hidden = 1,
    Boolean = 2,
    Linked = 3,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum LinkedIdType {
    LoginLinkedId(login::LoginLinkedId),
    CardLinkedId(card::CardLinkedId),
    IdentityLinkedId(identity::IdentityLinkedId),
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct FieldView {
    pub name: Option<String>,
    pub value: Option<String>,
    pub r#type: FieldType,
    pub show_value: bool,
    pub show_count: bool,
    pub linked_id: Option<LinkedIdType>,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct PasswordHistoryView {
    password: String,
    last_used_date: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherView {
    pub id: Uuid,
    pub organization_id: Option<Uuid>,
    pub folder_id: Option<Uuid>,

    pub name: String,
    pub notes: String,
    pub r#type: CipherType,

    pub login: Option<login::LoginView>,
    pub identity: Option<identity::IdentityView>,
    pub card: Option<card::CardView>,
    // pub secure_note: Option<SecureNoteView>, // We can probably handle this in the SDK only.

    //
    attachments: Vec<AttachmentView>,
    fields: Vec<FieldView>,
    password_history: Vec<PasswordHistoryView>,

    pub collection_ids: Vec<Uuid>,
    pub favorite: bool,
    pub reprompt: CipherRepromptType,

    pub creation_date: DateTime<Utc>,
    pub deleted_date: Option<DateTime<Utc>>,
    pub revision_date: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherListResponse {
    ciphers: Vec<CipherListView>,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherRequest {
    id: Uuid,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherCreateRequest {
    name: String,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherUpdateRequest {
    id: Uuid,
    name: String,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CipherDeleteRequest {
    id: Uuid,
}
