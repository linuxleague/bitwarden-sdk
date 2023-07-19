use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, JsonSchema)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub enum PasswordGeneratorRequest {
    Password {
        length: usize,

        lowercase: bool,
        uppercase: bool,
        numbers: bool,
        special: bool,
        minimum_numbers: usize,
        minimum_special: usize,

        avoid_ambiguous_characters: bool,
        exclude: String,
    },
    Passphrase {
        word_count: usize,
        word_separator: char,
        capitalize: bool,
        include_number: bool,
    },
}
