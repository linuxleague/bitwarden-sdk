use chrono::{DateTime, Utc};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum SendType {
    Text = 0,
    File = 1,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendTextView {
    hidden: bool,
    text: String,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendFileView {
    id: String,
    size: usize,
    name: String,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendView {
    id: Uuid,
    access_id: String,

    r#type: SendType,
    name: String,
    notes: String,

    file: Option<SendFileView>,
    text: Option<SendTextView>,

    // key: String,
    max_access_count: Option<i32>,
    access_count: i32,

    revision_date: DateTime<Utc>,
    expiration_date: Option<DateTime<Utc>>,
    deletion_date: Option<DateTime<Utc>>,

    password: Option<String>,
    disabled: bool,
    hide_email: bool,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendListResponse {
    folders: Vec<SendView>,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendRequest {
    id: Uuid,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendCreateRequest {
    r#type: SendType,
    name: String,
    notes: String,

    file: Option<SendFileView>,
    text: Option<SendTextView>,

    // key: String,
    max_access_count: Option<i32>,

    deletion_date: Option<DateTime<Utc>>,

    password: Option<String>,
    disabled: bool,
    hide_email: bool,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendUpdateRequest {
    id: Uuid,

    r#type: SendType,
    name: String,
    notes: String,

    file: Option<SendFileView>,
    text: Option<SendTextView>,

    //key: String,
    max_access_count: Option<i32>,
    access_count: i32,

    revision_date: DateTime<Utc>,
    expiration_date: Option<DateTime<Utc>>,
    deletion_date: Option<DateTime<Utc>>,

    password: Option<String>,
    disabled: bool,
    hide_email: bool,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct SendDeleteRequest {
    id: Uuid,
}
