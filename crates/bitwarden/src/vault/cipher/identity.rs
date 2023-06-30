use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct IdentityView {
    pub title: Option<String>,
    pub first_name: Option<String>,
    pub middle_name: Option<String>,
    pub last_name: Option<String>,
    pub address1: Option<String>,
    pub address2: Option<String>,
    pub address3: Option<String>,
    pub city: Option<String>,
    pub state: Option<String>,
    pub postal_code: Option<String>,
    pub country: Option<String>,
    pub company: Option<String>,
    pub email: Option<String>,
    pub phone: Option<String>,
    pub ssn: Option<String>,
    pub username: Option<String>,
    pub passport_number: Option<String>,
    pub license_number: Option<String>,
}

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum IdentityLinkedId {
    Title = 400,
    MiddleName = 401,
    Address1 = 402,
    Address2 = 403,
    Address3 = 404,
    City = 405,
    State = 406,
    PostalCode = 407,
    Country = 408,
    Company = 409,
    Email = 410,
    Phone = 411,
    Ssn = 412,
    Username = 413,
    PassportNumber = 414,
    LicenseNumber = 415,
    FirstName = 416,
    LastName = 417,
    FullName = 418,
}
