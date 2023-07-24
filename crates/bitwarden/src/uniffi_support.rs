use uniffi::{FfiConverter, MetadataBuffer, RustBuffer};

use crate::UniFfiTag;

// Could probably be replaced with https://github.com/mozilla/uniffi-rs/pull/1661
unsafe impl FfiConverter<UniFfiTag> for uuid::Uuid {
    uniffi::ffi_converter_default_return!(crate::UniFfiTag);

    type FfiType = RustBuffer;

    fn lower(obj: Self) -> Self::FfiType {
        <String as FfiConverter<UniFfiTag>>::lower(obj.to_string())
    }
    fn try_lift(v: Self::FfiType) -> uniffi::Result<Self> {
        let s = <String as FfiConverter<UniFfiTag>>::try_lift(v)?;
        Ok(Self::parse_str(&s)?)
    }
    fn write(obj: Self, buf: &mut Vec<u8>) {
        <String as FfiConverter<UniFfiTag>>::write(obj.to_string(), buf);
    }
    fn try_read(buf: &mut &[u8]) -> uniffi::Result<Self> {
        let s = <String as FfiConverter<UniFfiTag>>::try_read(buf)?;
        Ok(Self::parse_str(&s)?)
    }
    const TYPE_ID_META: MetadataBuffer =
        MetadataBuffer::from_code(uniffi::metadata::codes::TYPE_CUSTOM)
            .concat_str("bitwarden")
            .concat_str("Uuid")
            .concat(<String as FfiConverter<UniFfiTag>>::TYPE_ID_META);
}
