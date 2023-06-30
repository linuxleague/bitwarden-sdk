// To parse this data:
//
//   import { Convert, ClientSettings, Command, ResponseForAPIKeyLoginResponse, ResponseForCipherListResponse, ResponseForCipherView, ResponseForFolderResponse, ResponseForPasswordLoginResponse, ResponseForSecretIdentifiersResponse, ResponseForSecretResponse, ResponseForSecretsDeleteResponse, ResponseForSyncResponse, ResponseForUserAPIKeyResponse } from "./file";
//
//   const clientSettings = Convert.toClientSettings(json);
//   const command = Convert.toCommand(json);
//   const responseForAPIKeyLoginResponse = Convert.toResponseForAPIKeyLoginResponse(json);
//   const responseForCipherListResponse = Convert.toResponseForCipherListResponse(json);
//   const responseForCipherView = Convert.toResponseForCipherView(json);
//   const responseForFolderResponse = Convert.toResponseForFolderResponse(json);
//   const responseForPasswordLoginResponse = Convert.toResponseForPasswordLoginResponse(json);
//   const responseForSecretIdentifiersResponse = Convert.toResponseForSecretIdentifiersResponse(json);
//   const responseForSecretResponse = Convert.toResponseForSecretResponse(json);
//   const responseForSecretsDeleteResponse = Convert.toResponseForSecretsDeleteResponse(json);
//   const responseForSyncResponse = Convert.toResponseForSyncResponse(json);
//   const responseForUserAPIKeyResponse = Convert.toResponseForUserAPIKeyResponse(json);
//
// These functions will throw an error if the JSON doesn't
// match the expected interface, even if the JSON is valid.

/**
 * Basic client behavior settings. These settings specify the various targets and behavior
 * of the Bitwarden Client. They are optional and uneditable once the client is
 * initialized.
 *
 * Defaults to
 *
 * ``` # use bitwarden::client::client_settings::{ClientSettings, DeviceType}; # use
 * assert_matches::assert_matches; let settings = ClientSettings { identity_url:
 * "https://identity.bitwarden.com".to_string(), api_url:
 * "https://api.bitwarden.com".to_string(), user_agent: "Bitwarden Rust-SDK".to_string(),
 * device_type: DeviceType::SDK, }; let default = ClientSettings::default();
 * assert_matches!(settings, default); ```
 *
 * Targets `localhost:8080` for debug builds.
 */
export interface ClientSettings {
    /**
     * The api url of the targeted Bitwarden instance. Defaults to `https://api.bitwarden.com`
     */
    apiUrl: string;
    /**
     * Device type to send to Bitwarden. Defaults to SDK
     */
    deviceType: DeviceType;
    /**
     * The identity url of the targeted Bitwarden instance. Defaults to
     * `https://identity.bitwarden.com`
     */
    identityUrl: string;
    /**
     * The user_agent to sent to Bitwarden. Defaults to `Bitwarden Rust-SDK`
     */
    userAgent: string;
}

/**
 * Device type to send to Bitwarden. Defaults to SDK
 */
export enum DeviceType {
    Android = "Android",
    AndroidAmazon = "AndroidAmazon",
    ChromeBrowser = "ChromeBrowser",
    ChromeExtension = "ChromeExtension",
    EdgeBrowser = "EdgeBrowser",
    EdgeExtension = "EdgeExtension",
    FirefoxBrowser = "FirefoxBrowser",
    FirefoxExtension = "FirefoxExtension",
    IEBrowser = "IEBrowser",
    IOS = "iOS",
    LinuxDesktop = "LinuxDesktop",
    MACOSDesktop = "MacOsDesktop",
    OperaBrowser = "OperaBrowser",
    OperaExtension = "OperaExtension",
    SDK = "SDK",
    SafariBrowser = "SafariBrowser",
    SafariExtension = "SafariExtension",
    UWP = "UWP",
    UnknownBrowser = "UnknownBrowser",
    VivaldiBrowser = "VivaldiBrowser",
    VivaldiExtension = "VivaldiExtension",
    WindowsDesktop = "WindowsDesktop",
}

/**
 * Login with username and password
 *
 * This command is for initiating an authentication handshake with Bitwarden. Authorization
 * may fail due to requiring 2fa or captcha challenge completion despite accurate
 * credentials.
 *
 * This command is not capable of handling authentication requiring 2fa or captcha.
 *
 * Returns: [PasswordLoginResponse](crate::sdk::auth::response::PasswordLoginResponse)
 *
 * Login with API Key
 *
 * This command is for initiating an authentication handshake with Bitwarden.
 *
 * Returns: [ApiKeyLoginResponse](crate::sdk::auth::response::ApiKeyLoginResponse)
 *
 * Login with Secrets Manager Access Token
 *
 * This command is for initiating an authentication handshake with Bitwarden.
 *
 * Returns: [ApiKeyLoginResponse](crate::sdk::auth::response::ApiKeyLoginResponse)
 *
 * > Requires Authentication Get the API key of the currently authenticated user
 *
 * Returns:
 * [UserApiKeyResponse](crate::sdk::response::user_api_key_response::UserApiKeyResponse)
 *
 * Get the user's passphrase
 *
 * Returns: String
 *
 * > Requires Authentication Retrieve all user data, ciphers and organizations the user is a
 * part of
 *
 * Returns: [SyncResponse](crate::sdk::response::sync_response::SyncResponse)
 */
export interface Command {
    passwordLogin?:    PasswordLoginRequest;
    apiKeyLogin?:      APIKeyLoginRequest;
    accessTokenLogin?: AccessTokenLoginRequest;
    getUserApiKey?:    SecretVerificationRequest;
    fingerprint?:      FingerprintRequest;
    sync?:             SyncRequest;
    secrets?:          SecretsCommand;
    projects?:         ProjectsCommand;
    vault?:            VaultCommand;
}

/**
 * Login to Bitwarden with access token
 */
export interface AccessTokenLoginRequest {
    /**
     * Bitwarden service API access token
     */
    accessToken: string;
}

/**
 * Login to Bitwarden with Api Key
 */
export interface APIKeyLoginRequest {
    /**
     * Bitwarden account client_id
     */
    clientId: string;
    /**
     * Bitwarden account client_secret
     */
    clientSecret: string;
    /**
     * Bitwarden account master password
     */
    password: string;
}

export interface FingerprintRequest {
    /**
     * The input material, used in the fingerprint generation process.
     */
    fingerprintMaterial: string;
    /**
     * The user's public key
     */
    publicKey: string;
}

export interface SecretVerificationRequest {
    /**
     * The user's master password to use for user verification. If supplied, this will be used
     * for verification purposes.
     */
    masterPassword?: null | string;
    /**
     * Alternate user verification method through OTP. This is provided for users who have no
     * master password due to use of Customer Managed Encryption. Must be present and valid if
     * master_password is absent.
     */
    otp?: null | string;
}

/**
 * Login to Bitwarden with Username and Password
 */
export interface PasswordLoginRequest {
    /**
     * Bitwarden account email address
     */
    email: string;
    /**
     * Bitwarden account master password
     */
    password: string;
}

/**
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Retrieve a project by the provided identifier
 *
 * Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Creates a new project in the provided organization using the given data
 *
 * Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Lists all projects of the given organization
 *
 * Returns: [ProjectsResponse](crate::sdk::response::projects_response::ProjectsResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Updates an existing project with the provided ID using the given data
 *
 * Returns: [ProjectResponse](crate::sdk::response::projects_response::ProjectResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Deletes all the projects whose IDs match the provided ones
 *
 * Returns:
 * [ProjectsDeleteResponse](crate::sdk::response::projects_response::ProjectsDeleteResponse)
 */
export interface ProjectsCommand {
    get?:    ProjectGetRequest;
    create?: ProjectCreateRequest;
    list?:   ProjectsListRequest;
    update?: ProjectPutRequest;
    delete?: ProjectsDeleteRequest;
}

export interface ProjectCreateRequest {
    name: string;
    /**
     * Organization where the project will be created
     */
    organizationId: string;
}

export interface ProjectsDeleteRequest {
    /**
     * IDs of the projects to delete
     */
    ids: string[];
}

export interface ProjectGetRequest {
    /**
     * ID of the project to retrieve
     */
    id: string;
}

export interface ProjectsListRequest {
    /**
     * Organization to retrieve all the projects from
     */
    organizationId: string;
}

export interface ProjectPutRequest {
    /**
     * ID of the project to modify
     */
    id:   string;
    name: string;
    /**
     * Organization ID of the project to modify
     */
    organizationId: string;
}

/**
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Retrieve a secret by the provided identifier
 *
 * Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Creates a new secret in the provided organization using the given data
 *
 * Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Lists all secret identifiers of the given organization, to then retrieve each
 * secret, use `CreateSecret`
 *
 * Returns:
 * [SecretIdentifiersResponse](crate::sdk::response::secrets_response::SecretIdentifiersResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Updates an existing secret with the provided ID using the given data
 *
 * Returns: [SecretResponse](crate::sdk::response::secrets_response::SecretResponse)
 *
 * > Requires Authentication > Requires using an Access Token for login or calling Sync at
 * least once Deletes all the secrets whose IDs match the provided ones
 *
 * Returns:
 * [SecretsDeleteResponse](crate::sdk::response::secrets_response::SecretsDeleteResponse)
 */
export interface SecretsCommand {
    get?:    SecretGetRequest;
    create?: SecretCreateRequest;
    list?:   SecretIdentifiersRequest;
    update?: SecretPutRequest;
    delete?: SecretsDeleteRequest;
}

export interface SecretCreateRequest {
    key:  string;
    note: string;
    /**
     * Organization where the secret will be created
     */
    organizationId: string;
    /**
     * IDs of the projects that this secret will belong to
     */
    projectIds?: string[] | null;
    value:       string;
}

export interface SecretsDeleteRequest {
    /**
     * IDs of the secrets to delete
     */
    ids: string[];
}

export interface SecretGetRequest {
    /**
     * ID of the secret to retrieve
     */
    id: string;
}

export interface SecretIdentifiersRequest {
    /**
     * Organization to retrieve all the secrets from
     */
    organizationId: string;
}

export interface SecretPutRequest {
    /**
     * ID of the secret to modify
     */
    id:   string;
    key:  string;
    note: string;
    /**
     * Organization ID of the secret to modify
     */
    organizationId: string;
    value:          string;
}

export interface SyncRequest {
    /**
     * Exclude the subdomains from the response, defaults to false
     */
    excludeSubdomains?: boolean | null;
}

export interface VaultCommand {
    folders?: FoldersCommandClass | SCommand;
    items?:   ItemsCommandClass | SCommand;
}

/**
 * > Requires Authentication > Requires an unlocked vault Creates a new folder with the
 * provided data
 *
 * > Requires Authentication > Requires an unlocked vault and calling Sync at least once
 * Lists all folders in the vault
 *
 * Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
 *
 * > Requires Authentication > Requires an unlocked vault Updates an existing folder with
 * the provided data given its ID
 *
 * > Requires Authentication > Requires an unlocked vault Deletes the folder associated with
 * the provided ID
 */
export interface FoldersCommandClass {
    create?: FolderCreateRequest;
    get?:    FolderRequest;
    update?: FolderUpdateRequest;
    delete?: FolderDeleteRequest;
}

export interface FolderCreateRequest {
    name: string;
}

export interface FolderDeleteRequest {
    id: string;
}

export interface FolderRequest {
    id: string;
}

export interface FolderUpdateRequest {
    id:   string;
    name: string;
}

/**
 * > Requires Authentication > Requires an unlocked vault and calling Sync at least once
 * Lists all folders in the vault
 *
 * Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
 *
 * > Requires Authentication > Requires an unlocked vault and calling Sync at least once
 * Lists all items in the vault
 *
 * Returns: [CipherListResponse](bitwarden::vault::cipher::CipherListResponse)
 */
export enum SCommand {
    List = "list",
}

/**
 * > Requires Authentication > Requires an unlocked vault Creates a new item with the
 * provided data
 *
 * > Requires Authentication > Requires an unlocked vault and calling Sync at least once
 * Retrieves a single item in the vault
 *
 * Returns: [FoldersResponse](bitwarden::platform::folders::FoldersResponse)
 *
 * > Requires Authentication > Requires an unlocked vault Updates an existing item with the
 * provided data given its ID
 *
 * > Requires Authentication > Requires an unlocked vault Deletes the item associated with
 * the provided ID
 */
export interface ItemsCommandClass {
    create?: CipherCreateRequest;
    get?:    CipherRequest;
    update?: CipherUpdateRequest;
    delete?: CipherDeleteRequest;
}

export interface CipherCreateRequest {
    name: string;
}

export interface CipherDeleteRequest {
    id: string;
}

export interface CipherRequest {
    id: string;
}

export interface CipherUpdateRequest {
    id:   string;
    name: string;
}

export interface ResponseForAPIKeyLoginResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: APIKeyLoginResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface APIKeyLoginResponse {
    authenticated: boolean;
    /**
     * Whether or not the user is required to update their master password
     */
    forcePasswordReset: boolean;
    /**
     * TODO: What does this do?
     */
    resetMasterPassword: boolean;
    twoFactor?:          APIKeyLoginResponseTwoFactorProviders | null;
}

export interface APIKeyLoginResponseTwoFactorProviders {
    authenticator?: PurpleAuthenticator | null;
    /**
     * Duo-backed 2fa
     */
    duo?: PurpleDuo | null;
    /**
     * Email 2fa
     */
    email?: PurpleEmail | null;
    /**
     * Duo-backed 2fa operated by an organization the user is a member of
     */
    organizationDuo?: PurpleDuo | null;
    /**
     * Presence indicates the user has stored this device as bypassing 2fa
     */
    remember?: PurpleRemember | null;
    /**
     * WebAuthn-backed 2fa
     */
    webAuthn?: PurpleWebAuthn | null;
    /**
     * Yubikey-backed 2fa
     */
    yubiKey?: PurpleYubiKey | null;
}

export interface PurpleAuthenticator {
}

export interface PurpleDuo {
    host:      string;
    signature: string;
}

export interface PurpleEmail {
    /**
     * The email to request a 2fa TOTP for
     */
    email: string;
}

export interface PurpleRemember {
}

export interface PurpleWebAuthn {
}

export interface PurpleYubiKey {
    /**
     * Whether the stored yubikey supports near field communication
     */
    nfc: boolean;
}

export interface ResponseForCipherListResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: CipherListResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface CipherListResponse {
    ciphers: CipherListView[];
}

export interface CipherListView {
    collectionIds:   string[];
    creationDate:    Date;
    deletedDate?:    Date | null;
    favorite:        boolean;
    folderId?:       null | string;
    id:              string;
    name:            string;
    organizationId?: null | string;
    reprompt:        CipherRepromptType;
    revisionDate:    Date;
    subTitle?:       null | string;
    type:            CipherType;
}

export enum CipherRepromptType {
    None = "None",
    Password = "Password",
}

export enum CipherType {
    Card = "Card",
    Identity = "Identity",
    Login = "Login",
    SecureNote = "SecureNote",
}

export interface ResponseForCipherView {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: CipherView | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface CipherView {
    attachments:     AttachmentView[];
    card?:           CardView | null;
    collectionIds:   string[];
    creationDate:    Date;
    deletedDate?:    Date | null;
    favorite:        boolean;
    fields:          FieldView[];
    folderId?:       null | string;
    id:              string;
    identity?:       IdentityView | null;
    login?:          LoginView | null;
    name:            string;
    notes:           string;
    organizationId?: null | string;
    passwordHistory: PasswordHistoryView[];
    reprompt:        CipherRepromptType;
    revisionDate:    Date;
    type:            CipherType;
}

export interface AttachmentView {
    fileName?: null | string;
    id?:       null | string;
    key?:      null | string;
    size?:     null | string;
    sizeName?: null | string;
    url?:      null | string;
}

export interface CardView {
    brand?:          null | string;
    cardholderName?: null | string;
    code?:           null | string;
    expMonth?:       null | string;
    expYear?:        null | string;
    number?:         null | string;
}

export interface FieldView {
    linkedId?: LinkedIDType | null;
    name?:     null | string;
    showCount: boolean;
    showValue: boolean;
    type:      FieldType;
    value?:    null | string;
}

export interface LinkedIDType {
    loginLinkedId?:    LoginLinkedID;
    cardLinkedId?:     CardLinkedID;
    identityLinkedId?: IdentityLinkedID;
}

export enum CardLinkedID {
    Brand = "brand",
    CardholderName = "cardholderName",
    Code = "code",
    ExpMonth = "expMonth",
    ExpYear = "expYear",
    Number = "number",
}

export enum IdentityLinkedID {
    Address1 = "address1",
    Address2 = "address2",
    Address3 = "address3",
    City = "city",
    Company = "company",
    Country = "country",
    Email = "email",
    FirstName = "firstName",
    FullName = "fullName",
    LastName = "lastName",
    LicenseNumber = "licenseNumber",
    MiddleName = "middleName",
    PassportNumber = "passportNumber",
    Phone = "phone",
    PostalCode = "postalCode",
    Ssn = "ssn",
    State = "state",
    Title = "title",
    Username = "username",
}

export enum LoginLinkedID {
    Password = "password",
    Username = "username",
}

export enum FieldType {
    Boolean = "boolean",
    Hidden = "hidden",
    Linked = "linked",
    Text = "text",
}

export interface IdentityView {
    address1?:       null | string;
    address2?:       null | string;
    address3?:       null | string;
    city?:           null | string;
    company?:        null | string;
    country?:        null | string;
    email?:          null | string;
    firstName?:      null | string;
    lastName?:       null | string;
    licenseNumber?:  null | string;
    middleName?:     null | string;
    passportNumber?: null | string;
    phone?:          null | string;
    postalCode?:     null | string;
    ssn?:            null | string;
    state?:          null | string;
    title?:          null | string;
    username?:       null | string;
}

export interface LoginView {
    autofillOnPageLoad:    boolean;
    password:              string;
    passwordRevisionDate?: Date | null;
    totp?:                 null | string;
    uris:                  LoginURIView[];
    username:              string;
}

export interface LoginURIView {
    match: URIMatchType;
    uri:   string;
}

export enum URIMatchType {
    Domain = "domain",
    Exact = "exact",
    Host = "host",
    Never = "never",
    RegularExpression = "regularExpression",
    StartsWith = "startsWith",
}

export interface PasswordHistoryView {
    lastUsedDate: Date;
    password:     string;
}

export interface ResponseForFolderResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: FolderResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface FolderResponse {
    folder: FolderView;
}

export interface FolderView {
    id:           string;
    name:         string;
    revisionDate: Date;
}

export interface ResponseForPasswordLoginResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: PasswordLoginResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface PasswordLoginResponse {
    authenticated: boolean;
    /**
     * The information required to present the user with a captcha challenge. Only present when
     * authentication fails due to requiring validation of a captcha challenge.
     */
    captcha?: CAPTCHAResponse | null;
    /**
     * Whether or not the user is required to update their master password
     */
    forcePasswordReset: boolean;
    /**
     * TODO: What does this do?
     */
    resetMasterPassword: boolean;
    /**
     * The available two factor authentication options. Present only when authentication fails
     * due to requiring a second authentication factor.
     */
    twoFactor?: PasswordLoginResponseTwoFactorProviders | null;
}

export interface CAPTCHAResponse {
    /**
     * hcaptcha site key
     */
    siteKey: string;
}

export interface PasswordLoginResponseTwoFactorProviders {
    authenticator?: FluffyAuthenticator | null;
    /**
     * Duo-backed 2fa
     */
    duo?: FluffyDuo | null;
    /**
     * Email 2fa
     */
    email?: FluffyEmail | null;
    /**
     * Duo-backed 2fa operated by an organization the user is a member of
     */
    organizationDuo?: FluffyDuo | null;
    /**
     * Presence indicates the user has stored this device as bypassing 2fa
     */
    remember?: FluffyRemember | null;
    /**
     * WebAuthn-backed 2fa
     */
    webAuthn?: FluffyWebAuthn | null;
    /**
     * Yubikey-backed 2fa
     */
    yubiKey?: FluffyYubiKey | null;
}

export interface FluffyAuthenticator {
}

export interface FluffyDuo {
    host:      string;
    signature: string;
}

export interface FluffyEmail {
    /**
     * The email to request a 2fa TOTP for
     */
    email: string;
}

export interface FluffyRemember {
}

export interface FluffyWebAuthn {
}

export interface FluffyYubiKey {
    /**
     * Whether the stored yubikey supports near field communication
     */
    nfc: boolean;
}

export interface ResponseForSecretIdentifiersResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: SecretIdentifiersResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface SecretIdentifiersResponse {
    data: SecretIdentifierResponse[];
}

export interface SecretIdentifierResponse {
    id:             string;
    key:            string;
    organizationId: string;
}

export interface ResponseForSecretResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: SecretResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface SecretResponse {
    creationDate:   string;
    id:             string;
    key:            string;
    note:           string;
    object:         string;
    organizationId: string;
    projectId?:     null | string;
    revisionDate:   string;
    value:          string;
}

export interface ResponseForSecretsDeleteResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: SecretsDeleteResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface SecretsDeleteResponse {
    data: SecretDeleteResponse[];
}

export interface SecretDeleteResponse {
    error?: null | string;
    id:     string;
}

export interface ResponseForSyncResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: SyncResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface SyncResponse {
    /**
     * List of ciphers accesible by the user
     */
    ciphers: CipherDetailsResponse[];
    /**
     * Data about the user, including their encryption keys and the organizations they are a
     * part of
     */
    profile: ProfileResponse;
}

export interface CipherDetailsResponse {
}

/**
 * Data about the user, including their encryption keys and the organizations they are a
 * part of
 */
export interface ProfileResponse {
    email:         string;
    id:            string;
    name:          string;
    organizations: ProfileOrganizationResponse[];
}

export interface ProfileOrganizationResponse {
    id: string;
}

export interface ResponseForUserAPIKeyResponse {
    /**
     * The response data. Populated if `success` is true.
     */
    data?: UserAPIKeyResponse | null;
    /**
     * A message for any error that may occur. Populated if `success` is false.
     */
    errorMessage?: null | string;
    /**
     * Whether or not the SDK request succeeded.
     */
    success: boolean;
}

export interface UserAPIKeyResponse {
    /**
     * The user's API key, which represents the client_secret portion of an oauth request.
     */
    apiKey: string;
}

// Converts JSON strings to/from your types
// and asserts the results of JSON.parse at runtime
export class Convert {
    public static toClientSettings(json: string): ClientSettings {
        return cast(JSON.parse(json), r("ClientSettings"));
    }

    public static clientSettingsToJson(value: ClientSettings): string {
        return JSON.stringify(uncast(value, r("ClientSettings")), null, 2);
    }

    public static toCommand(json: string): Command {
        return cast(JSON.parse(json), r("Command"));
    }

    public static commandToJson(value: Command): string {
        return JSON.stringify(uncast(value, r("Command")), null, 2);
    }

    public static toResponseForAPIKeyLoginResponse(json: string): ResponseForAPIKeyLoginResponse {
        return cast(JSON.parse(json), r("ResponseForAPIKeyLoginResponse"));
    }

    public static responseForAPIKeyLoginResponseToJson(value: ResponseForAPIKeyLoginResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForAPIKeyLoginResponse")), null, 2);
    }

    public static toResponseForCipherListResponse(json: string): ResponseForCipherListResponse {
        return cast(JSON.parse(json), r("ResponseForCipherListResponse"));
    }

    public static responseForCipherListResponseToJson(value: ResponseForCipherListResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForCipherListResponse")), null, 2);
    }

    public static toResponseForCipherView(json: string): ResponseForCipherView {
        return cast(JSON.parse(json), r("ResponseForCipherView"));
    }

    public static responseForCipherViewToJson(value: ResponseForCipherView): string {
        return JSON.stringify(uncast(value, r("ResponseForCipherView")), null, 2);
    }

    public static toResponseForFolderResponse(json: string): ResponseForFolderResponse {
        return cast(JSON.parse(json), r("ResponseForFolderResponse"));
    }

    public static responseForFolderResponseToJson(value: ResponseForFolderResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForFolderResponse")), null, 2);
    }

    public static toResponseForPasswordLoginResponse(json: string): ResponseForPasswordLoginResponse {
        return cast(JSON.parse(json), r("ResponseForPasswordLoginResponse"));
    }

    public static responseForPasswordLoginResponseToJson(value: ResponseForPasswordLoginResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForPasswordLoginResponse")), null, 2);
    }

    public static toResponseForSecretIdentifiersResponse(json: string): ResponseForSecretIdentifiersResponse {
        return cast(JSON.parse(json), r("ResponseForSecretIdentifiersResponse"));
    }

    public static responseForSecretIdentifiersResponseToJson(value: ResponseForSecretIdentifiersResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForSecretIdentifiersResponse")), null, 2);
    }

    public static toResponseForSecretResponse(json: string): ResponseForSecretResponse {
        return cast(JSON.parse(json), r("ResponseForSecretResponse"));
    }

    public static responseForSecretResponseToJson(value: ResponseForSecretResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForSecretResponse")), null, 2);
    }

    public static toResponseForSecretsDeleteResponse(json: string): ResponseForSecretsDeleteResponse {
        return cast(JSON.parse(json), r("ResponseForSecretsDeleteResponse"));
    }

    public static responseForSecretsDeleteResponseToJson(value: ResponseForSecretsDeleteResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForSecretsDeleteResponse")), null, 2);
    }

    public static toResponseForSyncResponse(json: string): ResponseForSyncResponse {
        return cast(JSON.parse(json), r("ResponseForSyncResponse"));
    }

    public static responseForSyncResponseToJson(value: ResponseForSyncResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForSyncResponse")), null, 2);
    }

    public static toResponseForUserAPIKeyResponse(json: string): ResponseForUserAPIKeyResponse {
        return cast(JSON.parse(json), r("ResponseForUserAPIKeyResponse"));
    }

    public static responseForUserAPIKeyResponseToJson(value: ResponseForUserAPIKeyResponse): string {
        return JSON.stringify(uncast(value, r("ResponseForUserAPIKeyResponse")), null, 2);
    }
}

function invalidValue(typ: any, val: any, key: any, parent: any = ''): never {
    const prettyTyp = prettyTypeName(typ);
    const parentText = parent ? ` on ${parent}` : '';
    const keyText = key ? ` for key "${key}"` : '';
    throw Error(`Invalid value${keyText}${parentText}. Expected ${prettyTyp} but got ${JSON.stringify(val)}`);
}

function prettyTypeName(typ: any): string {
    if (Array.isArray(typ)) {
        if (typ.length === 2 && typ[0] === undefined) {
            return `an optional ${prettyTypeName(typ[1])}`;
        } else {
            return `one of [${typ.map(a => { return prettyTypeName(a); }).join(", ")}]`;
        }
    } else if (typeof typ === "object" && typ.literal !== undefined) {
        return typ.literal;
    } else {
        return typeof typ;
    }
}

function jsonToJSProps(typ: any): any {
    if (typ.jsonToJS === undefined) {
        const map: any = {};
        typ.props.forEach((p: any) => map[p.json] = { key: p.js, typ: p.typ });
        typ.jsonToJS = map;
    }
    return typ.jsonToJS;
}

function jsToJSONProps(typ: any): any {
    if (typ.jsToJSON === undefined) {
        const map: any = {};
        typ.props.forEach((p: any) => map[p.js] = { key: p.json, typ: p.typ });
        typ.jsToJSON = map;
    }
    return typ.jsToJSON;
}

function transform(val: any, typ: any, getProps: any, key: any = '', parent: any = ''): any {
    function transformPrimitive(typ: string, val: any): any {
        if (typeof typ === typeof val) return val;
        return invalidValue(typ, val, key, parent);
    }

    function transformUnion(typs: any[], val: any): any {
        // val must validate against one typ in typs
        const l = typs.length;
        for (let i = 0; i < l; i++) {
            const typ = typs[i];
            try {
                return transform(val, typ, getProps);
            } catch (_) {}
        }
        return invalidValue(typs, val, key, parent);
    }

    function transformEnum(cases: string[], val: any): any {
        if (cases.indexOf(val) !== -1) return val;
        return invalidValue(cases.map(a => { return l(a); }), val, key, parent);
    }

    function transformArray(typ: any, val: any): any {
        // val must be an array with no invalid elements
        if (!Array.isArray(val)) return invalidValue(l("array"), val, key, parent);
        return val.map(el => transform(el, typ, getProps));
    }

    function transformDate(val: any): any {
        if (val === null) {
            return null;
        }
        const d = new Date(val);
        if (isNaN(d.valueOf())) {
            return invalidValue(l("Date"), val, key, parent);
        }
        return d;
    }

    function transformObject(props: { [k: string]: any }, additional: any, val: any): any {
        if (val === null || typeof val !== "object" || Array.isArray(val)) {
            return invalidValue(l(ref || "object"), val, key, parent);
        }
        const result: any = {};
        Object.getOwnPropertyNames(props).forEach(key => {
            const prop = props[key];
            const v = Object.prototype.hasOwnProperty.call(val, key) ? val[key] : undefined;
            result[prop.key] = transform(v, prop.typ, getProps, key, ref);
        });
        Object.getOwnPropertyNames(val).forEach(key => {
            if (!Object.prototype.hasOwnProperty.call(props, key)) {
                result[key] = transform(val[key], additional, getProps, key, ref);
            }
        });
        return result;
    }

    if (typ === "any") return val;
    if (typ === null) {
        if (val === null) return val;
        return invalidValue(typ, val, key, parent);
    }
    if (typ === false) return invalidValue(typ, val, key, parent);
    let ref: any = undefined;
    while (typeof typ === "object" && typ.ref !== undefined) {
        ref = typ.ref;
        typ = typeMap[typ.ref];
    }
    if (Array.isArray(typ)) return transformEnum(typ, val);
    if (typeof typ === "object") {
        return typ.hasOwnProperty("unionMembers") ? transformUnion(typ.unionMembers, val)
            : typ.hasOwnProperty("arrayItems")    ? transformArray(typ.arrayItems, val)
            : typ.hasOwnProperty("props")         ? transformObject(getProps(typ), typ.additional, val)
            : invalidValue(typ, val, key, parent);
    }
    // Numbers can be parsed by Date but shouldn't be.
    if (typ === Date && typeof val !== "number") return transformDate(val);
    return transformPrimitive(typ, val);
}

function cast<T>(val: any, typ: any): T {
    return transform(val, typ, jsonToJSProps);
}

function uncast<T>(val: T, typ: any): any {
    return transform(val, typ, jsToJSONProps);
}

function l(typ: any) {
    return { literal: typ };
}

function a(typ: any) {
    return { arrayItems: typ };
}

function u(...typs: any[]) {
    return { unionMembers: typs };
}

function o(props: any[], additional: any) {
    return { props, additional };
}

function m(additional: any) {
    return { props: [], additional };
}

function r(name: string) {
    return { ref: name };
}

const typeMap: any = {
    "ClientSettings": o([
        { json: "apiUrl", js: "apiUrl", typ: "" },
        { json: "deviceType", js: "deviceType", typ: r("DeviceType") },
        { json: "identityUrl", js: "identityUrl", typ: "" },
        { json: "userAgent", js: "userAgent", typ: "" },
    ], false),
    "Command": o([
        { json: "passwordLogin", js: "passwordLogin", typ: u(undefined, r("PasswordLoginRequest")) },
        { json: "apiKeyLogin", js: "apiKeyLogin", typ: u(undefined, r("APIKeyLoginRequest")) },
        { json: "accessTokenLogin", js: "accessTokenLogin", typ: u(undefined, r("AccessTokenLoginRequest")) },
        { json: "getUserApiKey", js: "getUserApiKey", typ: u(undefined, r("SecretVerificationRequest")) },
        { json: "fingerprint", js: "fingerprint", typ: u(undefined, r("FingerprintRequest")) },
        { json: "sync", js: "sync", typ: u(undefined, r("SyncRequest")) },
        { json: "secrets", js: "secrets", typ: u(undefined, r("SecretsCommand")) },
        { json: "projects", js: "projects", typ: u(undefined, r("ProjectsCommand")) },
        { json: "vault", js: "vault", typ: u(undefined, r("VaultCommand")) },
    ], false),
    "AccessTokenLoginRequest": o([
        { json: "accessToken", js: "accessToken", typ: "" },
    ], false),
    "APIKeyLoginRequest": o([
        { json: "clientId", js: "clientId", typ: "" },
        { json: "clientSecret", js: "clientSecret", typ: "" },
        { json: "password", js: "password", typ: "" },
    ], false),
    "FingerprintRequest": o([
        { json: "fingerprintMaterial", js: "fingerprintMaterial", typ: "" },
        { json: "publicKey", js: "publicKey", typ: "" },
    ], false),
    "SecretVerificationRequest": o([
        { json: "masterPassword", js: "masterPassword", typ: u(undefined, u(null, "")) },
        { json: "otp", js: "otp", typ: u(undefined, u(null, "")) },
    ], false),
    "PasswordLoginRequest": o([
        { json: "email", js: "email", typ: "" },
        { json: "password", js: "password", typ: "" },
    ], false),
    "ProjectsCommand": o([
        { json: "get", js: "get", typ: u(undefined, r("ProjectGetRequest")) },
        { json: "create", js: "create", typ: u(undefined, r("ProjectCreateRequest")) },
        { json: "list", js: "list", typ: u(undefined, r("ProjectsListRequest")) },
        { json: "update", js: "update", typ: u(undefined, r("ProjectPutRequest")) },
        { json: "delete", js: "delete", typ: u(undefined, r("ProjectsDeleteRequest")) },
    ], false),
    "ProjectCreateRequest": o([
        { json: "name", js: "name", typ: "" },
        { json: "organizationId", js: "organizationId", typ: "" },
    ], false),
    "ProjectsDeleteRequest": o([
        { json: "ids", js: "ids", typ: a("") },
    ], false),
    "ProjectGetRequest": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "ProjectsListRequest": o([
        { json: "organizationId", js: "organizationId", typ: "" },
    ], false),
    "ProjectPutRequest": o([
        { json: "id", js: "id", typ: "" },
        { json: "name", js: "name", typ: "" },
        { json: "organizationId", js: "organizationId", typ: "" },
    ], false),
    "SecretsCommand": o([
        { json: "get", js: "get", typ: u(undefined, r("SecretGetRequest")) },
        { json: "create", js: "create", typ: u(undefined, r("SecretCreateRequest")) },
        { json: "list", js: "list", typ: u(undefined, r("SecretIdentifiersRequest")) },
        { json: "update", js: "update", typ: u(undefined, r("SecretPutRequest")) },
        { json: "delete", js: "delete", typ: u(undefined, r("SecretsDeleteRequest")) },
    ], false),
    "SecretCreateRequest": o([
        { json: "key", js: "key", typ: "" },
        { json: "note", js: "note", typ: "" },
        { json: "organizationId", js: "organizationId", typ: "" },
        { json: "projectIds", js: "projectIds", typ: u(undefined, u(a(""), null)) },
        { json: "value", js: "value", typ: "" },
    ], false),
    "SecretsDeleteRequest": o([
        { json: "ids", js: "ids", typ: a("") },
    ], false),
    "SecretGetRequest": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "SecretIdentifiersRequest": o([
        { json: "organizationId", js: "organizationId", typ: "" },
    ], false),
    "SecretPutRequest": o([
        { json: "id", js: "id", typ: "" },
        { json: "key", js: "key", typ: "" },
        { json: "note", js: "note", typ: "" },
        { json: "organizationId", js: "organizationId", typ: "" },
        { json: "value", js: "value", typ: "" },
    ], false),
    "SyncRequest": o([
        { json: "excludeSubdomains", js: "excludeSubdomains", typ: u(undefined, u(true, null)) },
    ], false),
    "VaultCommand": o([
        { json: "folders", js: "folders", typ: u(undefined, u(r("FoldersCommandClass"), r("SCommand"))) },
        { json: "items", js: "items", typ: u(undefined, u(r("ItemsCommandClass"), r("SCommand"))) },
    ], false),
    "FoldersCommandClass": o([
        { json: "create", js: "create", typ: u(undefined, r("FolderCreateRequest")) },
        { json: "get", js: "get", typ: u(undefined, r("FolderRequest")) },
        { json: "update", js: "update", typ: u(undefined, r("FolderUpdateRequest")) },
        { json: "delete", js: "delete", typ: u(undefined, r("FolderDeleteRequest")) },
    ], false),
    "FolderCreateRequest": o([
        { json: "name", js: "name", typ: "" },
    ], false),
    "FolderDeleteRequest": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "FolderRequest": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "FolderUpdateRequest": o([
        { json: "id", js: "id", typ: "" },
        { json: "name", js: "name", typ: "" },
    ], false),
    "ItemsCommandClass": o([
        { json: "create", js: "create", typ: u(undefined, r("CipherCreateRequest")) },
        { json: "get", js: "get", typ: u(undefined, r("CipherRequest")) },
        { json: "update", js: "update", typ: u(undefined, r("CipherUpdateRequest")) },
        { json: "delete", js: "delete", typ: u(undefined, r("CipherDeleteRequest")) },
    ], false),
    "CipherCreateRequest": o([
        { json: "name", js: "name", typ: "" },
    ], false),
    "CipherDeleteRequest": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "CipherRequest": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "CipherUpdateRequest": o([
        { json: "id", js: "id", typ: "" },
        { json: "name", js: "name", typ: "" },
    ], false),
    "ResponseForAPIKeyLoginResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("APIKeyLoginResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "APIKeyLoginResponse": o([
        { json: "authenticated", js: "authenticated", typ: true },
        { json: "forcePasswordReset", js: "forcePasswordReset", typ: true },
        { json: "resetMasterPassword", js: "resetMasterPassword", typ: true },
        { json: "twoFactor", js: "twoFactor", typ: u(undefined, u(r("APIKeyLoginResponseTwoFactorProviders"), null)) },
    ], false),
    "APIKeyLoginResponseTwoFactorProviders": o([
        { json: "authenticator", js: "authenticator", typ: u(undefined, u(r("PurpleAuthenticator"), null)) },
        { json: "duo", js: "duo", typ: u(undefined, u(r("PurpleDuo"), null)) },
        { json: "email", js: "email", typ: u(undefined, u(r("PurpleEmail"), null)) },
        { json: "organizationDuo", js: "organizationDuo", typ: u(undefined, u(r("PurpleDuo"), null)) },
        { json: "remember", js: "remember", typ: u(undefined, u(r("PurpleRemember"), null)) },
        { json: "webAuthn", js: "webAuthn", typ: u(undefined, u(r("PurpleWebAuthn"), null)) },
        { json: "yubiKey", js: "yubiKey", typ: u(undefined, u(r("PurpleYubiKey"), null)) },
    ], false),
    "PurpleAuthenticator": o([
    ], false),
    "PurpleDuo": o([
        { json: "host", js: "host", typ: "" },
        { json: "signature", js: "signature", typ: "" },
    ], false),
    "PurpleEmail": o([
        { json: "email", js: "email", typ: "" },
    ], false),
    "PurpleRemember": o([
    ], false),
    "PurpleWebAuthn": o([
    ], false),
    "PurpleYubiKey": o([
        { json: "nfc", js: "nfc", typ: true },
    ], false),
    "ResponseForCipherListResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("CipherListResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "CipherListResponse": o([
        { json: "ciphers", js: "ciphers", typ: a(r("CipherListView")) },
    ], false),
    "CipherListView": o([
        { json: "collectionIds", js: "collectionIds", typ: a("") },
        { json: "creationDate", js: "creationDate", typ: Date },
        { json: "deletedDate", js: "deletedDate", typ: u(undefined, u(Date, null)) },
        { json: "favorite", js: "favorite", typ: true },
        { json: "folderId", js: "folderId", typ: u(undefined, u(null, "")) },
        { json: "id", js: "id", typ: "" },
        { json: "name", js: "name", typ: "" },
        { json: "organizationId", js: "organizationId", typ: u(undefined, u(null, "")) },
        { json: "reprompt", js: "reprompt", typ: r("CipherRepromptType") },
        { json: "revisionDate", js: "revisionDate", typ: Date },
        { json: "subTitle", js: "subTitle", typ: u(undefined, u(null, "")) },
        { json: "type", js: "type", typ: r("CipherType") },
    ], false),
    "ResponseForCipherView": o([
        { json: "data", js: "data", typ: u(undefined, u(r("CipherView"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "CipherView": o([
        { json: "attachments", js: "attachments", typ: a(r("AttachmentView")) },
        { json: "card", js: "card", typ: u(undefined, u(r("CardView"), null)) },
        { json: "collectionIds", js: "collectionIds", typ: a("") },
        { json: "creationDate", js: "creationDate", typ: Date },
        { json: "deletedDate", js: "deletedDate", typ: u(undefined, u(Date, null)) },
        { json: "favorite", js: "favorite", typ: true },
        { json: "fields", js: "fields", typ: a(r("FieldView")) },
        { json: "folderId", js: "folderId", typ: u(undefined, u(null, "")) },
        { json: "id", js: "id", typ: "" },
        { json: "identity", js: "identity", typ: u(undefined, u(r("IdentityView"), null)) },
        { json: "login", js: "login", typ: u(undefined, u(r("LoginView"), null)) },
        { json: "name", js: "name", typ: "" },
        { json: "notes", js: "notes", typ: "" },
        { json: "organizationId", js: "organizationId", typ: u(undefined, u(null, "")) },
        { json: "passwordHistory", js: "passwordHistory", typ: a(r("PasswordHistoryView")) },
        { json: "reprompt", js: "reprompt", typ: r("CipherRepromptType") },
        { json: "revisionDate", js: "revisionDate", typ: Date },
        { json: "type", js: "type", typ: r("CipherType") },
    ], false),
    "AttachmentView": o([
        { json: "fileName", js: "fileName", typ: u(undefined, u(null, "")) },
        { json: "id", js: "id", typ: u(undefined, u(null, "")) },
        { json: "key", js: "key", typ: u(undefined, u(null, "")) },
        { json: "size", js: "size", typ: u(undefined, u(null, "")) },
        { json: "sizeName", js: "sizeName", typ: u(undefined, u(null, "")) },
        { json: "url", js: "url", typ: u(undefined, u(null, "")) },
    ], false),
    "CardView": o([
        { json: "brand", js: "brand", typ: u(undefined, u(null, "")) },
        { json: "cardholderName", js: "cardholderName", typ: u(undefined, u(null, "")) },
        { json: "code", js: "code", typ: u(undefined, u(null, "")) },
        { json: "expMonth", js: "expMonth", typ: u(undefined, u(null, "")) },
        { json: "expYear", js: "expYear", typ: u(undefined, u(null, "")) },
        { json: "number", js: "number", typ: u(undefined, u(null, "")) },
    ], false),
    "FieldView": o([
        { json: "linkedId", js: "linkedId", typ: u(undefined, u(r("LinkedIDType"), null)) },
        { json: "name", js: "name", typ: u(undefined, u(null, "")) },
        { json: "showCount", js: "showCount", typ: true },
        { json: "showValue", js: "showValue", typ: true },
        { json: "type", js: "type", typ: r("FieldType") },
        { json: "value", js: "value", typ: u(undefined, u(null, "")) },
    ], false),
    "LinkedIDType": o([
        { json: "loginLinkedId", js: "loginLinkedId", typ: u(undefined, r("LoginLinkedID")) },
        { json: "cardLinkedId", js: "cardLinkedId", typ: u(undefined, r("CardLinkedID")) },
        { json: "identityLinkedId", js: "identityLinkedId", typ: u(undefined, r("IdentityLinkedID")) },
    ], false),
    "IdentityView": o([
        { json: "address1", js: "address1", typ: u(undefined, u(null, "")) },
        { json: "address2", js: "address2", typ: u(undefined, u(null, "")) },
        { json: "address3", js: "address3", typ: u(undefined, u(null, "")) },
        { json: "city", js: "city", typ: u(undefined, u(null, "")) },
        { json: "company", js: "company", typ: u(undefined, u(null, "")) },
        { json: "country", js: "country", typ: u(undefined, u(null, "")) },
        { json: "email", js: "email", typ: u(undefined, u(null, "")) },
        { json: "firstName", js: "firstName", typ: u(undefined, u(null, "")) },
        { json: "lastName", js: "lastName", typ: u(undefined, u(null, "")) },
        { json: "licenseNumber", js: "licenseNumber", typ: u(undefined, u(null, "")) },
        { json: "middleName", js: "middleName", typ: u(undefined, u(null, "")) },
        { json: "passportNumber", js: "passportNumber", typ: u(undefined, u(null, "")) },
        { json: "phone", js: "phone", typ: u(undefined, u(null, "")) },
        { json: "postalCode", js: "postalCode", typ: u(undefined, u(null, "")) },
        { json: "ssn", js: "ssn", typ: u(undefined, u(null, "")) },
        { json: "state", js: "state", typ: u(undefined, u(null, "")) },
        { json: "title", js: "title", typ: u(undefined, u(null, "")) },
        { json: "username", js: "username", typ: u(undefined, u(null, "")) },
    ], false),
    "LoginView": o([
        { json: "autofillOnPageLoad", js: "autofillOnPageLoad", typ: true },
        { json: "password", js: "password", typ: "" },
        { json: "passwordRevisionDate", js: "passwordRevisionDate", typ: u(undefined, u(Date, null)) },
        { json: "totp", js: "totp", typ: u(undefined, u(null, "")) },
        { json: "uris", js: "uris", typ: a(r("LoginURIView")) },
        { json: "username", js: "username", typ: "" },
    ], false),
    "LoginURIView": o([
        { json: "match", js: "match", typ: r("URIMatchType") },
        { json: "uri", js: "uri", typ: "" },
    ], false),
    "PasswordHistoryView": o([
        { json: "lastUsedDate", js: "lastUsedDate", typ: Date },
        { json: "password", js: "password", typ: "" },
    ], false),
    "ResponseForFolderResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("FolderResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "FolderResponse": o([
        { json: "folder", js: "folder", typ: r("FolderView") },
    ], false),
    "FolderView": o([
        { json: "id", js: "id", typ: "" },
        { json: "name", js: "name", typ: "" },
        { json: "revisionDate", js: "revisionDate", typ: Date },
    ], false),
    "ResponseForPasswordLoginResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("PasswordLoginResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "PasswordLoginResponse": o([
        { json: "authenticated", js: "authenticated", typ: true },
        { json: "captcha", js: "captcha", typ: u(undefined, u(r("CAPTCHAResponse"), null)) },
        { json: "forcePasswordReset", js: "forcePasswordReset", typ: true },
        { json: "resetMasterPassword", js: "resetMasterPassword", typ: true },
        { json: "twoFactor", js: "twoFactor", typ: u(undefined, u(r("PasswordLoginResponseTwoFactorProviders"), null)) },
    ], false),
    "CAPTCHAResponse": o([
        { json: "siteKey", js: "siteKey", typ: "" },
    ], false),
    "PasswordLoginResponseTwoFactorProviders": o([
        { json: "authenticator", js: "authenticator", typ: u(undefined, u(r("FluffyAuthenticator"), null)) },
        { json: "duo", js: "duo", typ: u(undefined, u(r("FluffyDuo"), null)) },
        { json: "email", js: "email", typ: u(undefined, u(r("FluffyEmail"), null)) },
        { json: "organizationDuo", js: "organizationDuo", typ: u(undefined, u(r("FluffyDuo"), null)) },
        { json: "remember", js: "remember", typ: u(undefined, u(r("FluffyRemember"), null)) },
        { json: "webAuthn", js: "webAuthn", typ: u(undefined, u(r("FluffyWebAuthn"), null)) },
        { json: "yubiKey", js: "yubiKey", typ: u(undefined, u(r("FluffyYubiKey"), null)) },
    ], false),
    "FluffyAuthenticator": o([
    ], false),
    "FluffyDuo": o([
        { json: "host", js: "host", typ: "" },
        { json: "signature", js: "signature", typ: "" },
    ], false),
    "FluffyEmail": o([
        { json: "email", js: "email", typ: "" },
    ], false),
    "FluffyRemember": o([
    ], false),
    "FluffyWebAuthn": o([
    ], false),
    "FluffyYubiKey": o([
        { json: "nfc", js: "nfc", typ: true },
    ], false),
    "ResponseForSecretIdentifiersResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("SecretIdentifiersResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "SecretIdentifiersResponse": o([
        { json: "data", js: "data", typ: a(r("SecretIdentifierResponse")) },
    ], false),
    "SecretIdentifierResponse": o([
        { json: "id", js: "id", typ: "" },
        { json: "key", js: "key", typ: "" },
        { json: "organizationId", js: "organizationId", typ: "" },
    ], false),
    "ResponseForSecretResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("SecretResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "SecretResponse": o([
        { json: "creationDate", js: "creationDate", typ: "" },
        { json: "id", js: "id", typ: "" },
        { json: "key", js: "key", typ: "" },
        { json: "note", js: "note", typ: "" },
        { json: "object", js: "object", typ: "" },
        { json: "organizationId", js: "organizationId", typ: "" },
        { json: "projectId", js: "projectId", typ: u(undefined, u(null, "")) },
        { json: "revisionDate", js: "revisionDate", typ: "" },
        { json: "value", js: "value", typ: "" },
    ], false),
    "ResponseForSecretsDeleteResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("SecretsDeleteResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "SecretsDeleteResponse": o([
        { json: "data", js: "data", typ: a(r("SecretDeleteResponse")) },
    ], false),
    "SecretDeleteResponse": o([
        { json: "error", js: "error", typ: u(undefined, u(null, "")) },
        { json: "id", js: "id", typ: "" },
    ], false),
    "ResponseForSyncResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("SyncResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "SyncResponse": o([
        { json: "ciphers", js: "ciphers", typ: a(r("CipherDetailsResponse")) },
        { json: "profile", js: "profile", typ: r("ProfileResponse") },
    ], false),
    "CipherDetailsResponse": o([
    ], false),
    "ProfileResponse": o([
        { json: "email", js: "email", typ: "" },
        { json: "id", js: "id", typ: "" },
        { json: "name", js: "name", typ: "" },
        { json: "organizations", js: "organizations", typ: a(r("ProfileOrganizationResponse")) },
    ], false),
    "ProfileOrganizationResponse": o([
        { json: "id", js: "id", typ: "" },
    ], false),
    "ResponseForUserAPIKeyResponse": o([
        { json: "data", js: "data", typ: u(undefined, u(r("UserAPIKeyResponse"), null)) },
        { json: "errorMessage", js: "errorMessage", typ: u(undefined, u(null, "")) },
        { json: "success", js: "success", typ: true },
    ], false),
    "UserAPIKeyResponse": o([
        { json: "apiKey", js: "apiKey", typ: "" },
    ], false),
    "DeviceType": [
        "Android",
        "AndroidAmazon",
        "ChromeBrowser",
        "ChromeExtension",
        "EdgeBrowser",
        "EdgeExtension",
        "FirefoxBrowser",
        "FirefoxExtension",
        "IEBrowser",
        "iOS",
        "LinuxDesktop",
        "MacOsDesktop",
        "OperaBrowser",
        "OperaExtension",
        "SDK",
        "SafariBrowser",
        "SafariExtension",
        "UWP",
        "UnknownBrowser",
        "VivaldiBrowser",
        "VivaldiExtension",
        "WindowsDesktop",
    ],
    "SCommand": [
        "list",
    ],
    "CipherRepromptType": [
        "None",
        "Password",
    ],
    "CipherType": [
        "Card",
        "Identity",
        "Login",
        "SecureNote",
    ],
    "CardLinkedID": [
        "brand",
        "cardholderName",
        "code",
        "expMonth",
        "expYear",
        "number",
    ],
    "IdentityLinkedID": [
        "address1",
        "address2",
        "address3",
        "city",
        "company",
        "country",
        "email",
        "firstName",
        "fullName",
        "lastName",
        "licenseNumber",
        "middleName",
        "passportNumber",
        "phone",
        "postalCode",
        "ssn",
        "state",
        "title",
        "username",
    ],
    "LoginLinkedID": [
        "password",
        "username",
    ],
    "FieldType": [
        "boolean",
        "hidden",
        "linked",
        "text",
    ],
    "URIMatchType": [
        "domain",
        "exact",
        "host",
        "never",
        "regularExpression",
        "startsWith",
    ],
};

